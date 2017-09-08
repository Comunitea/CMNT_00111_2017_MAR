# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import logging
import time
from datetime import datetime

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools import float_is_zero
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
import openerp.addons.product.product

_logger = logging.getLogger(__name__)

class pos_coupons(osv.osv):
    _inherit = 'pos.coupons'
    def _get_dft_currency(self, cr, uid, ctx=None):
        comp = self.pool.get('res.users').browse(cr,uid,uid).company_id
        if not comp:
            comp_id = self.pool.get('res.company').search(cr, uid, [])[0]
            comp = self.pool.get('res.company').browse(cr, uid, comp_id)
        return comp.currency_id      
    def _price_incl(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        coupons_config_obj = self.pool.get('pos.coupons.config')
        coupons_config = False
        coupons_config_id = coupons_config_obj.search(cr, uid, [], context=context)
        if coupons_config_id:
            coupons_config = coupons_config_obj.browse(cr, uid, coupons_config_id[0], context=context)
        res = {}
        if context is None:
            context = {}

        for xxxx in self.browse(cr, uid, ids, context=context):
            price = xxxx.coupon_value
            if coupons_config:
                taxes = tax_obj.compute_all(cr, uid, coupons_config.product_id.taxes_id, price, 1.0, coupons_config.product_id.id, False)
                cur = self._get_dft_currency(cr, uid, ctx=None)
                res[xxxx.id] = cur_obj.round(cr, uid, cur, taxes['total_included'])
            else:
                res[xxxx.id] = xxxx.coupon_value
        return res
        

    _columns = {
            'order_id': fields.many2one('pos.order', 'Pedido'),
            'origin_order_id': fields.many2one('pos.order', 'Pedido Original'),	        
            'coupon_value_incl':fields.function(_price_incl, type='float', string='Precio (Con IVA)', digits=(16, 2)),
             }
             
             
class pos_config(osv.osv):
    _inherit = 'pos.config'


    _columns = {
        'direccion_tienda': fields.char('Direccion tienda'),
        'direccion_tienda2': fields.char('Direccion tienda2'),        
        'direccion_tienda3': fields.char('Direccion tienda3'),        
        'direccion_tienda4': fields.char('Direccion tienda4'),         
        'account_bank_id': fields.many2one('account.account', 'Cuenta clientes banco', required=True) ,   
        'account_cash_id': fields.many2one('account.account', 'Cuenta clientes efectivo', required=True) ,   
        'account_tax_id': fields.many2one('account.account', 'Cuenta impuestos', required=True) ,   
        'account_mer_id': fields.many2one('account.account', 'Cuenta mercaderias', required=True) ,   
        'account_vale_id': fields.many2one('account.account', 'Cuenta Vales', required=True) ,   
        'account_vale_contr_id': fields.many2one('account.account', 'Cuenta Contrapartida Vales', required=True) ,   
        'account_cash_contr_id': fields.many2one('account.account', 'Cuenta Contrapartida Efectivo', required=True) ,   
        'journal_id': fields.many2one('account.journal', 'Diario', required=True) ,   
        
    }






class pos_order(osv.osv):
    _inherit = 'pos.order'


    #no crearemos los apuntes contables
    def _create_account_move_line(self, cr, uid, ids, session=None, move_id=None, context=None):
        return True
        
    _columns = {
        'coupon_id': fields.many2one('pos.coupons', 'Cupon', required=False),
        'origin_order_id': fields.many2one('pos.order', 'Orden original', required=False),
        'refund_type': fields.selection([('normal', 'Normal'),
                                   ('cupon', 'Cupon')],
                                  'Tipo Devolucion', readonly=False,required=True, copy=False),
                                  
                                  
    }   
    
    _defaults = {
        'refund_type': 'normal'
    }     
    
    def refund2(self, cr, uid, ids, context=None):
        """Create a copy of order  for refund order"""
        clone_list = []
        line_obj = self.pool.get('pos.order.line')
        
        for order in self.browse(cr, uid, ids, context=context):
            current_session_ids = self.pool.get('pos.session').search(cr, uid, [
                ('state', '!=', 'closed'),
                ('config_id.name', 'ilike', 'DEVOLUCIONES'),
                ('config_id.stock_location_id','=',order.session_id.config_id.stock_location_id.id)], context=context)
            if not current_session_ids:
                raise osv.except_osv(_('Error!'), _('Para devolver los producto necesita una sesion de devoluciones para este TPV.'))

            clone_id = self.copy(cr, uid, order.id, {
                'name': order.name + ' REFUND', # not used, name forced by create
                'session_id': current_session_ids[0],
                'date_order': time.strftime('%Y-%m-%d %H:%M:%S'),
                'refund_type':'cupon',
                'origin_order_id':order.id
            }, context=context)
            clone_list.append(clone_id)

        for clone in self.browse(cr, uid, clone_list, context=context):
            for order_line in clone.lines:
                line_obj.write(cr, uid, [order_line.id], {
                    'qty': -order_line.qty
                }, context=context)

        abs = {
            'name': _('Return Products'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pos.order',
            'res_id':clone_list[0],
            'view_id': False,
            'context':context,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
        }
        return abs

    def action_paid2(self, cr, uid, ids, context=None):
        #CREAMOS EL CUPON DESCUENTO
        coupon_obj = self.pool.get('pos.coupons')
        order_obj = self.pool.get('pos.order')
        order = order_obj.browse(cr, uid, ids, context=context)
        vals = {
                'name': 'Cupon descuento',
                'create_date': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'issue_date': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'validity': -1,
                'total_available': 1,
                'coupon_value': abs(order.amount_total-order.amount_tax),
                'note': 'Ticket :' + order.origin_order_id.pos_reference,
                'active': True,
                'user_id': uid,
                'origin_order_id':order.origin_order_id.id,
                'order_id':order.id
                }
        coupon = coupon_obj.create(cr, uid, vals, context=context)
        #creamos el apunte contable

        hoy = ((datetime.now()).date()).strftime('%Y-%m-%d')
        period_id = self.pool['account.period'].find(cr, uid, dt=hoy, context=context)
        period_id = period_id[0]

        vals = {'ref': 'Cupon Ticket :' + order.origin_order_id.pos_reference, 
                'journal_id': order.origin_order_id.session_id.config_id.journal_id.id, 
                'period_id': period_id,
                'date': hoy
                }
        move_id = self.pool.get('account.move').create(cr, uid, vals, context=context)  
                                                    
        #mercaderias
        lie_vals={
                 'name': 'Cupon Ticket :' + order.origin_order_id.pos_reference,
                 'date': hoy,
                 'ref': 'Cupon Ticket :' + order.origin_order_id.pos_reference,
                 'move_id': move_id,
                 'account_id': order.origin_order_id.session_id.config_id.account_vale_contr_id.id,
                 'credit': 0.0,
                 'debit': abs(order.amount_total),
                 'journal_id': order.origin_order_id.session_id.config_id.journal_id.id,
                 'period_id': period_id,
               }
        self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)    
        #VALE        
        lie_vals={
                 'name': 'Cupon Ticket :' + order.origin_order_id.pos_reference,
                 'date': hoy,
                 'ref': 'Cupon Ticket :' + order.origin_order_id.pos_reference,
                 'move_id': move_id,
                 'account_id': order.origin_order_id.session_id.config_id.account_vale_id.id,
                 'credit': abs(order.amount_total),
                 'debit': 0.0,
                 'journal_id': order.origin_order_id.session_id.config_id.journal_id.id,
                 'period_id': period_id,
               }
        self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)    

        
        
        
        
        self.write(cr, uid, ids, {'state': 'paid','coupon_id':coupon}, context=context)
        self.create_picking(cr, uid, ids, context=context)

 
        
        
        return True
        
class pos_session(osv.osv):
    _inherit = 'pos.session'
    def crea_asiento(self, cr, uid, ids, context=None): 
        for record in self.browse(cr, uid, ids, context=context):
            print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            pedidos = []
            for st in record.statement_ids:
                print 'st'
                print st
                for st_line in st.line_ids:
                    #print 'line_ids'  
                    #print st_line.pos_statement_id.name
                    if st_line.pos_statement_id:
                        if st_line.pos_statement_id.id not in pedidos:
                            pedidos.append(st_line.pos_statement_id.id)
                            print st_line.pos_statement_id.id
            base = 0.0
            bank = 0.0
            cash = 0.0
            tax = 0.0
            total = 0.0
            for pedido in self.pool.get('pos.order').browse(cr, uid, pedidos, context=context):
                print 'pedido'
                print pedido.name
                total = pedido.amount_total
                tax = tax + pedido.amount_tax
                base = + base + pedido.amount_total - pedido.amount_tax
                if pedido.statement_ids[0].journal_id.type == 'bank':
                    print 'banco'
                    print total
                    bank = bank + total
                if pedido.statement_ids[0].journal_id.type == 'cash':
                    print 'cash'
                    print total
                    cash = cash + total
            period_id = self.pool['account.period'].find(cr, uid, dt=record.stop_at, context=context)

            period_id = period_id[0]

            ref = (datetime.strptime(record.stop_at, '%Y-%m-%d %H:%M:%S').date()).strftime('%d-%m-%Y')
            vals = {'ref': record.config_id.name + ' ' + ref, 
                    'journal_id': record.config_id.journal_id.id, 
                    'period_id': period_id,
                    'date': record.stop_at
                    }
            move_id = self.pool.get('account.move').create(cr, uid, vals, context=context)  
                                                    
            #mercaderias
            lie_vals={
                     'name': record.config_id.name + ' ' + ref, 
                     'date': record.stop_at,
                     'ref': record.config_id.name + ' ' + ref, 
                     'move_id': move_id,
                     'account_id': record.config_id.account_mer_id.id,
                     'credit': base,
                     'debit': 0.0,
                     'journal_id': record.config_id.journal_id.id,
                     'period_id': period_id,
                     #'currency_id': amount_currency and cur_id,
                     #'amount_currency': amount_currency,
                   }
            self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)    
            #impuestos
            lie_vals={
                     'name': record.config_id.name + ' ' + ref, 
                     'date': record.stop_at,
                     'ref': record.config_id.name + ' ' + ref, 
                     'move_id': move_id,
                     'account_id': record.config_id.account_tax_id.id,
                     'credit': tax,
                     'debit': 0.0,
                     'journal_id': record.config_id.journal_id.id,
                     'period_id': period_id,
                     #'currency_id': amount_currency and cur_id,
                     #'amount_currency': amount_currency,
                   } 
            self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)  
            #cash
            lie_vals={
                     'name': record.config_id.name + ' ' + ref, 
                     'date': record.stop_at,
                     'ref': record.config_id.name + ' ' + ref, 
                     'move_id': move_id,
                     'account_id': record.config_id.account_cash_id.id,
                     'credit': 0.0,
                     'debit': cash,
                     'journal_id': record.config_id.journal_id.id,
                     'period_id': period_id,
                     #'currency_id': amount_currency and cur_id,
                     #'amount_currency': amount_currency,
                   }
            self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)  
            #bank
            lie_vals={
                     'name': record.config_id.name + ' ' + ref, 
                     'date': record.stop_at,
                     'ref': record.config_id.name + ' ' + ref, 
                     'move_id': move_id,
                     'account_id': record.config_id.account_bank_id.id,
                     'credit': 0.0,
                     'debit': bank,
                     'journal_id': record.config_id.journal_id.id,
                     'period_id': period_id,
                     #'currency_id': amount_currency and cur_id,
                     #'amount_currency': amount_currency,
                   } 
            self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)                                                               
            #cash contra
            lie_vals={
                     'name': record.config_id.name + ' ' + ref, 
                     'date': record.stop_at,
                     'ref': record.config_id.name + ' ' + ref, 
                     'move_id': move_id,
                     'account_id': record.config_id.account_cash_id.id,
                     'credit': cash,
                     'debit': 0.0,
                     'journal_id': record.config_id.journal_id.id,
                     'period_id': period_id,
                     #'currency_id': amount_currency and cur_id,
                     #'amount_currency': amount_currency,
                   }
            self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)   
            #cash contra 570
            lie_vals={
                     'name': record.config_id.name + ' ' + ref, 
                     'date': record.stop_at,
                     'ref': record.config_id.name + ' ' + ref, 
                     'move_id': move_id,
                     'account_id': record.config_id.account_cash_contr_id.id,
                     'credit': 0.0,
                     'debit': cash,
                     'journal_id': record.config_id.journal_id.id,
                     'period_id': period_id,
                     #'currency_id': amount_currency and cur_id,
                     #'amount_currency': amount_currency,
                   }
            self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)             
                      
            self.write(cr, uid, [record.id], {'move_id':move_id}, context=context)
      
    #no crearemos los apuntes contables
    def wkf_action_close(self, cr, uid, ids, context=None):
        # Close CashBox
        for record in self.browse(cr, uid, ids, context=context):
            for st in record.statement_ids:
                if abs(st.difference) > st.journal_id.amount_authorized_diff:
                    # The pos manager can close statements with maximums.
                    if not self.pool.get('ir.model.access').check_groups(cr, uid, "point_of_sale.group_pos_manager"):
                        raise osv.except_osv( _('Error!'),
                            _("Your ending balance is too different from the theoretical cash closing (%.2f), the maximum allowed is: %.2f. You can contact your manager to force it.") % (st.difference, st.journal_id.amount_authorized_diff))
                if (st.journal_id.type not in ['bank', 'cash']):
                    raise osv.except_osv(_('Error!'), 
                        _("The type of the journal for your payment method should be bank or cash "))
                #getattr(st, 'button_confirm_%s' % st.journal_id.type)(context=context)
            self.crea_asiento(cr, uid, [record.id], context=context) 
        self._confirm_orders(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'state' : 'closed'}, context=context)

        obj = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'point_of_sale', 'menu_point_root')[1]
        return {
            'type' : 'ir.actions.client',
            'name' : 'Point of Sale Menu',
            'tag' : 'reload',
            'params' : {'menu_id': obj},
        }    
    def _create_account_move_line(self, cr, uid, ids, session=None, move_id=None, context=None):
        return True
    def _confirm_orders(self, cr, uid, ids, context=None):

        print 'ggggg _confirm_orders MIO'
        _logger.info('============ggggg _confirm_orders MIO================')
        _logger.info('============ggggg _confirm_orders MIO================')
        _logger.info('============ggggg _confirm_orders MIO================')
        pos_order_obj = self.pool.get('pos.order')
        for session in self.browse(cr, uid, ids, context=context):
            company_id = session.config_id.journal_id.company_id.id
            local_context = dict(context or {}, force_company=company_id)
            order_ids = [order.id for order in session.order_ids if order.state == 'paid']
            #no hacemos los apuntes, haremos un customizado
            #move_id = pos_order_obj._create_account_move(cr, uid, session.start_at, session.name, session.config_id.journal_id.id, company_id, context=context)
            #pos_order_obj._create_account_move_line(cr, uid, order_ids, session, move_id, context=local_context)

            for order in session.order_ids:
                if order.state == 'done':
                    continue
                if order.state not in ('paid', 'invoiced'):
                    raise osv.except_osv(
                        _('Error!'),
                        _("You cannot confirm all orders of this session, because they have not the 'paid' status"))
                else:
                    pos_order_obj.signal_workflow(cr, uid, [order.id], 'done')

        return True   
        
    _columns = {
        'move_id': fields.many2one('account.move', 'Apunte', required=False) ,   
        
    }

class pos_order_line(osv.osv):
    _inherit = 'pos.order.line'


    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        new_id = super(pos_order_line, self).create(cr, uid, vals=vals, context=context)
        try:
            if vals.get('product_id'):
                coupons_config_obj = self.pool.get('pos.coupons.config')
                order_obj = self.pool.get('pos.order')
                order_line_obj = self.pool.get('pos.order.line')
                coupons_config = False
                coupons_config_id = coupons_config_obj.search(cr, uid, [], context=context)
                order = order_obj.browse(cr, uid, vals.get('order_id'), context=context)
                order_line = order_line_obj.browse(cr, uid, new_id, context=context)
                amount_line_all = order_line_obj._amount_line_all(cr, uid, [order_line.id], field_names=['price_subtotal', 'price_subtotal_incl'], arg=None, context=context)
                price_subtotal_incl = amount_line_all[order_line.id]['price_subtotal_incl']
                print 'price_subtotal_incl'
                print price_subtotal_incl
                if coupons_config_id:
                    coupons_config = coupons_config_obj.browse(cr, uid, coupons_config_id[0], context=context)
                    product_coupon = coupons_config.product_id.id
                    if (vals.get('product_id')==product_coupon):
                        #realizamos el apunte
                        print 'realizamos el apunte'
                        hoy = ((datetime.now()).date()).strftime('%Y-%m-%d')
                        period_id = self.pool['account.period'].find(cr, uid, dt=hoy, context=context)
                        period_id = period_id[0]
                        vals = {'ref': 'Aplicado Cupon Ticket :' + order.pos_reference, 
                                'journal_id': order.session_id.config_id.journal_id.id, 
                                'period_id': period_id,
                                'date': hoy
                                }
                        move_id = self.pool.get('account.move').create(cr, uid, vals, context=context)  
                        #mercaderias
                        lie_vals={
                                 'name': 'Aplicado Cupon Ticket :' + order.pos_reference,
                                 'date': hoy,
                                 'ref': 'Aplicado Cupon Ticket :' + order.pos_reference,
                                 'move_id': move_id,
                                 'account_id': order.session_id.config_id.account_vale_contr_id.id,
                                 'credit': abs(price_subtotal_incl),
                                 'debit': 0.0,
                                 'journal_id': order.session_id.config_id.journal_id.id,
                                 'period_id': period_id,
                               }
                        self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)    
                        #VALE        
                        lie_vals={
                                 'name': 'Aplicado Cupon Ticket :' + order.pos_reference,
                                 'date': hoy,
                                 'ref': 'Aplicado Cupon Ticket :' + order.pos_reference,
                                 'move_id': move_id,
                                 'account_id': order.session_id.config_id.account_vale_id.id,
                                 'credit': 0.0,
                                 'debit': abs(price_subtotal_incl),
                                 'journal_id': order.session_id.config_id.journal_id.id,
                                 'period_id': period_id,
                               }
                        self.pool.get('account.move.line').create(cr, uid, lie_vals, context=context)  
        except:
            return new_id
        return new_id

 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
