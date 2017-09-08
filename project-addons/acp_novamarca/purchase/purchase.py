# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2008 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Jordi Esteve <jesteve@zikzakmedia.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime
import openerp.addons.product.product
import logging
import time
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class purchase_order(osv.osv):
    _inherit = 'purchase.order'
purchase_order()


class purchase_order_add(osv.osv_memory):


    _name = 'purchase.order.add'
    _columns = {
        'product_tmpl_id': fields.many2one('product.template', 'Modelo', required=True),
        'lines': fields.one2many('purchase.order.add.line','tmp_id', 'Productos')        
    }

    def product_tmpl_change(self, cr, uid, ids, product_tmpl_id, context=None):
        v = {}
        print self.browse(cr, uid, ids, context=context) 

        if product_tmpl_id:
            ids_p = self.pool.get('product.product').search(cr, uid, [('product_tmpl_id','=',product_tmpl_id)], context=context)
            v['lines'] = []
            for i in ids_p:

                v['lines'].append((0, 0,  { 'product_id':i }))

        return {'value': v}
        			

    def add(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('purchase.order')
        line_obj = self.pool.get('purchase.order.line')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')        
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids, context=context)[0]
        line_ids = [line.id for line in data.lines]
        if not line_ids:
            return {'type': 'ir.actions.act_window_close'}

        order = order_obj.browse(cr, uid, context['active_id'], context=context)

        ## Finally populate the current order with new lines:
        date_order = order.date_order
        partner_id = order.partner_id and order.partner_id.id or False
        pricelist_id = order.pricelist_id and order.pricelist_id.id or False
        fiscal_position_id = order.partner_id.property_account_position and order.partner_id.property_account_position.id or False
        if not date_order:
            date_order = fields.date.context_today(self,cr,uid,context=context)        
        for line in data.lines:
            if line.qty == 0.0:
                continue

            product = self.pool.get('product.product').browse(cr, uid, line.product_id.id, context=context)
            supplierinfo = False
            precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
            for supplier in product.seller_ids:
                if partner_id and (supplier.name.id == partner_id):
                    supplierinfo = supplier
            print 'supplierinfo'
            print supplierinfo
            print 'date_order'
            print date_order
            dt = line_obj._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            print 'dt'
            print dt

            # - determine price_unit and taxes_id
            if pricelist_id:
                price = product_pricelist.price_get(cr, uid, [pricelist_id],
                        product.id, line.qty or 1.0, partner_id or False, {'uom': line.product_id.uom_po_id.id, 'date': date_order})[pricelist_id]
            else:
                price = product.standard_price
    
            taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
            fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
            taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
            print 'taxes_ids'
            print taxes_ids

                
            line_obj.create(cr, uid,{
                    'order_id': order.id,
                    'product_qty': line.qty,
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'product_uom': line.product_id.uom_po_id.id,
                    'date_planned': dt,
                    'price_unit': price,
                    'taxes_id': [(6, 0, taxes_ids)],
                }, context=context)
        return {'type': 'ir.actions.act_window_close'}


purchase_order_add()  


class purchase_order_add_line(osv.osv_memory):


    _name = 'purchase.order.add.line'
    _columns = {
        'tmp_id': fields.many2one('purchase.order.add', 'Modelo', required=True) ,   
        'product_id': fields.many2one('product.product', 'Variantes de producto', required=True),
        'qty': fields.float('Cantidad', digits=(16, 2)),        
    }

purchase_order_add_line()    
