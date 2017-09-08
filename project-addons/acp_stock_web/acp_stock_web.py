# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import workflow
from time import strptime
import time
import urllib2
from lxml import etree
from openerp import tools

class acp_stock_web(osv.osv):
    _name = "acp_stock_web"

    _columns = {
        'company_id': fields.char('Url'),

    }
   

    def run_sync_jim(self, cr, uid, context=None):
        if context is None:
            context = {}
        inventory_obj = self.pool.get('stock.inventory')
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        inventory_line_obj = self.pool.get('stock.inventory.line')
        location_id = location_obj.search(cr, uid,[('name','=','Existencias JIM')],context=context)
        if len(location_id) > 0:
            location_id = location_obj.browse(cr, uid,location_id[0],context=context)
        else:
            raise osv.except_osv(_('Warning!'), _('No se encuentra almacen para JIM.'))
        print "<<<<<<<<<<<<<<<<<<<<<< run_sync_JIM"                               
        data = urllib2.urlopen('http://resources.jimsports.website/Intranet4/fich-stock-b2b.csv') # it's a file like object and works just like a file
        for line in data: # files are iterable
           line_split = line.split(';')
           
           code = line_split[0] #itemcode
           qty = line_split[2] #stock
           name = line_split[4] #name

           
           product_id = product_obj.search(cr, uid,[('default_code','=',code)],context=context)
         
           if len(product_id) > 0:
               product_id = product_obj.browse(cr, uid,product_id[0],context=context)

           else:
               product_id= False
           
           if product_id:

               if qty < 0:
                   raise osv.except_osv(_('Warning!'), _('Quantity cannot be negative.'))
               ctx = context.copy()
               ctx['location'] = location_id.id
               ctx['lot_id'] = ''
               product = product_id.with_context(location=location_id.id, lot_id= False)
               th_qty = product.qty_available
               
               if th_qty <> qty:
                   inventory_id = inventory_obj.create(cr, uid, {
                       'name': _('INV: %s') % tools.ustr(product_id.name),
                       'product_id': product_id.id,
                       'location_id': location_id.id,
                       'lot_id': ''}, context=context)
                   line_data = {
                       'inventory_id': inventory_id,
                       'product_qty': qty,
                       'location_id': location_id.id,
                       'product_id': product_id.id,
                       'product_uom_id': product_id.uom_id.id,
                       'theoretical_qty': th_qty,
                       'prod_lot_id': False
                   }
                   inventory_line_obj.create(cr , uid, line_data, context=context)
                   inventory_obj.action_done(cr, uid, [inventory_id], context=context)
                 
        return True

    
    def run_sync_roly(self, cr, uid, context=None):
        if context is None:
            context = {}
        inventory_obj = self.pool.get('stock.inventory')
        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')
        inventory_line_obj = self.pool.get('stock.inventory.line')
        location_id = location_obj.search(cr, uid,[('name','=','Existencias ROLY')],context=context)
        if len(location_id) > 0:
            location_id = location_obj.browse(cr, uid,location_id[0],context=context)
        else:
            raise osv.except_osv(_('Warning!'), _('No se encuentra almacen para roly.'))
        print "<<<<<<<<<<<<<<<<<<<<<< run_sync_roly"                               
        data = urllib2.urlopen('http://www.roly.es/Downloads/stock.xls') # it's a file like object and works just like a file
        for line in data: # files are iterable
           #print line
           pos1 =line.find('<tr><td>');
           pos2 =line.find('</td><td>');
           pos3 =line.find('</td><td>',pos2+9);
           pos4 =line.find('</td><td>',pos3+9);

           code = line[pos1+8:pos2]
           name = line[pos2+9:pos3]
           qty = line[pos3+9:pos4]
           
           product_id = product_obj.search(cr, uid,[('default_code','=',code)],context=context)
         
           if len(product_id) > 0:
               product_id = product_obj.browse(cr, uid,product_id[0],context=context)

           else:
               product_id= False
           
           if product_id:

               if qty < 0:
                   raise osv.except_osv(_('Warning!'), _('Quantity cannot be negative.'))
               ctx = context.copy()
               ctx['location'] = location_id.id
               ctx['lot_id'] = ''
               product = product_id.with_context(location=location_id.id, lot_id= False)
               th_qty = product.qty_available
               
               if th_qty <> qty:
                   inventory_id = inventory_obj.create(cr, uid, {
                       'name': _('INV: %s') % tools.ustr(product_id.name),
                       'product_id': product_id.id,
                       'location_id': location_id.id,
                       'lot_id': ''}, context=context)
                   line_data = {
                       'inventory_id': inventory_id,
                       'product_qty': qty,
                       'location_id': location_id.id,
                       'product_id': product_id.id,
                       'product_uom_id': product_id.uom_id.id,
                       'theoretical_qty': th_qty,
                       'prod_lot_id': False
                   }
                   inventory_line_obj.create(cr , uid, line_data, context=context)
                   inventory_obj.action_done(cr, uid, [inventory_id], context=context)
               
        return True
                
           
           
