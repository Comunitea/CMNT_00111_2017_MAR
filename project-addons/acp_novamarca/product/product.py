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
from openerp.osv import fields, osv , orm
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval
import openerp.addons.decimal_precision as dp


class product_marca(osv.osv):


    _name = "product.marca"
    _columns = {
        'name':fields.char('Marca', size=256, readonly=False),
            
    }

 

product_marca()


    
class product_template(osv.osv):


    _inherit = "product.template"
    
    def _product_price_antes_incl(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')

        res = {}
        if context is None:
            context = {}

        for product in self.browse(cr, uid, ids, context=context):
            price = product.precio_antes
            taxes = tax_obj.compute_all(cr, uid, product.taxes_id, price, 1.0, product.id, False)
            cur = self._get_dft_currency(cr, uid, ctx=None)
            res[product.id] = cur_obj.round(cr, uid, cur, taxes['total_included'])
        return res
    def _product_price_incl(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')

        res = {}
        if context is None:
            context = {}

        for product in self.browse(cr, uid, ids, context=context):
            price = product.lst_price
            taxes = tax_obj.compute_all(cr, uid, product.taxes_id, price, 1.0, product.id, False)
            cur = self._get_dft_currency(cr, uid, ctx=None)
            res[product.id] = cur_obj.round(cr, uid, cur, taxes['total_included'])
        return res  
    
    def _get_dft_currency(self, cr, uid, ctx=None):
        comp = self.pool.get('res.users').browse(cr,uid,uid).company_id
        if not comp:
            comp_id = self.pool.get('res.company').search(cr, uid, [])[0]
            comp = self.pool.get('res.company').browse(cr, uid, comp_id)
        return comp.currency_id                    
    _columns = {
        'code':fields.char('Codigo', size=256, readonly=False,help="Este codigo se usa para generar el cdigo EAN de la variante"),
        'marca_id':fields.many2one('product.marca', 'Marca', required=True),
        'variant_model_name': fields.char('Variant Model Name', size=64, required=True,
                                          help=('[_o.dimension_id.name_] will be replaced with the'
                                                ' name of the dimension and [_o.option_id.code_] '
                                                'by the code of the option. Example of Variant '
                                                'Model Name : "[_o.dimension_id.name_] - '
                                                '[_o.option_id.code_]"')),
        'variant_model_name_separator': fields.char('Variant Model Name Separator', size=64,
                                                    help=('Add a separator between the elements '
                                                          'of the variant name')),
        'code_generator': fields.char('Code Generator', size=256,
                                      help=('enter the model for the product code, all parameter'
                                            ' between [_o.my_field_] will be replace by the '
                                            'product field. Example product_code model : '
                                            'prefix_[_o.variants_]_suffixe ==> result : '
                                            'prefix_2S2T_suffix')),        
        'precio_antes':fields.float('Precio Antes', digits_compute=dp.get_precision('Product Price')),                                                               
        'precio_antes_incl':fields.function(_product_price_antes_incl, type='float', string='Precio antes(Con IVA)', digits_compute=dp.get_precision('Product Price')),
        'precio_incl': fields.function(_product_price_incl, type='float', string='Precio (Con IVA)', digits_compute=dp.get_precision('Product Price')),        
        'default_code' : fields.char('Internal Reference', select=True),
    }

    def create(self, cr, uid, vals, context=None):
        vals['code'] = self.pool.get('ir.sequence').get(cr, uid, 'product.template') or '/'
        return super(product_template, self).create(cr, uid, vals, context=context)

    _defaults = {
        'variant_model_name': '[_o.option_id.name_]',
        'variant_model_name_separator': ' ',
        #'is_multi_variants': True,
        'code_generator': '',
    }
 

product_template()


class product_product(osv.osv):


    _inherit = "product.product"
    
    
    def _talla(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        # The current user may not have access rights for sale orders
        print '_talla'
        
        
        for product in self.browse(cr, uid, ids, context):
            talla = ''
            for dimension in product.dimension_value_ids:


                if dimension.option_id.dimension_id.tipo == 'TALLA':
                    talla = dimension.name
            res[product.id] = talla
 
        return res 
    def _color(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        # The current user may not have access rights for sale orders
        try:
            for product in self.browse(cr, uid, ids, context):
                color = ''
                for dimension in product.dimension_value_ids:
                    if dimension.option_id.dimension_id.tipo == 'COLOR':
                        color = dimension.name
                res[product.id] = color
        except:
            pass
        return res
        
    def _precio(self, cr, uid, ids, field_name, args, context=None):
        res = dict.fromkeys(ids, False)
        for this in self.browse(cr, uid, ids, context=context):
                res[this.id] = ""+"{:10.2f}".format(this.lst_price).replace('.', ',') + " €" 
        return res
    def _precio_antes(self, cr, uid, ids, field_name, args, context=None):
        res = dict.fromkeys(ids, False)
        for this in self.browse(cr, uid, ids, context=context):
                if this.precio_antes > 0.0:
                    res[this.id] = ""+"{:10.2f}".format(this.precio_antes).replace('.', ',') + " €" 
                else:
                    res[this.id] = "" 
        return res

    def _precio_incl(self, cr, uid, ids, field_name, args, context=None):
        res = dict.fromkeys(ids, False)
        for this in self.browse(cr, uid, ids, context=context):
                res[this.id] = ""+"{:10.2f}".format(this.precio_incl).replace('.', ',') + " €" 
        return res
    def _precio_antes_incl(self, cr, uid, ids, field_name, args, context=None):
        res = dict.fromkeys(ids, False)
        for this in self.browse(cr, uid, ids, context=context):
                if this.precio_antes > 0.0:
                    res[this.id] = ""+"{:10.2f}".format(this.precio_antes_incl).replace('.', ',') + " €" 
                else:
                    res[this.id] = "" 
        return res
    def _precio_antes_incl_label(self, cr, uid, ids, field_name, args, context=None):
        res = dict.fromkeys(ids, False)
        for this in self.browse(cr, uid, ids, context=context):
                if this.precio_antes > 0.0:
                    res[this.id] = "ANTES:"
                else:
                    res[this.id] = "" 
        return res        
    def _product_price_incl(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')

        res = {}
        if context is None:
            context = {}

        for product in self.browse(cr, uid, ids, context=context):
            price = product.lst_price
            taxes = tax_obj.compute_all(cr, uid, product.taxes_id, price, 1.0, product.id, False)
            cur = self._get_dft_currency(cr, uid, ctx=None)
            res[product.id] = cur_obj.round(cr, uid, cur, taxes['total_included'])
        return res  

    def _get_dft_currency(self, cr, uid, ctx=None):
        comp = self.pool.get('res.users').browse(cr,uid,uid).company_id
        if not comp:
            comp_id = self.pool.get('res.company').search(cr, uid, [])[0]
            comp = self.pool.get('res.company').browse(cr, uid, comp_id)
        return comp.currency_id  
    _columns = {
        'code':fields.char('Codigo1', size=256, readonly=False,help="Este codigo se usa para generar el cdigo EAN de la variante"),
        'marca_id':fields.related('product_tmpl_id', 'marca_id', type="many2one", relation="product.marca", string="Marca"),        
        'talla': fields.function(_talla, string='Talla', type='char'),        
        'color': fields.function(_color, string='Color', type='char'), 
        'precio_incl': fields.function(_product_price_incl, type='float', string='Precio (Con IVA)', digits_compute=dp.get_precision('Product Price')),        

                
        'precio_antes':fields.related('product_tmpl_id', 'precio_antes', type="float", string="Precio antes"),        
        'precio_antes_incl':fields.related('product_tmpl_id', 'precio_antes_incl', type="float", string="Precio antes(Con IVA)"),                
        
        'precio_txt':fields.function(_precio, string='Precio', type='char'), 
        'precio_incl_txt':fields.function(_precio_incl, string='Precio', type='char'), 
                
        'precio_antes_txt':fields.function(_precio_antes, string='Precio antes', type='char'),         
        'precio_antes_incl_txt':fields.function(_precio_antes_incl, string='Precio antes', type='char'),         
        'precio_antes_incl_txt_label':fields.function(_precio_antes_incl_label, string='Precio antes', type='char'),         
    }

    def create(self, cr, uid, vals, context=None):
        product_template = self.pool.get('product.template')
        product_obj = self.pool.get('product.product')
        dim_values_obj = self.pool.get('product.variant.dimension.value')
        t = vals.get('product_tmpl_id',False)
        if t:
            code = product_template.browse(cr, uid, t, context=context).code
            cr.execute('select count(1) from product_product where product_tmpl_id = %s',(t,))
            ean13_2 = cr.fetchone()[0] + 1
            code_complete = code + str(ean13_2).zfill(5)
            vals['ean13'] = openerp.addons.product.product.sanitize_ean13(code_complete)




        res = super(product_product, self).create(cr, uid, vals, context=context)

        return res
    def generate_product_code(self, cr, uid, product_obj, code_generator, context=None):


        color = False
        talla = False
            
        pt = product_obj.product_tmpl_id
        if product_obj.dimension_value_ids:

            for dimension in product_obj.dimension_value_ids:
                if dimension.option_id.dimension_id.tipo == 'TALLA':
                    talla = dimension.option_id.code 

            for dimension in product_obj.dimension_value_ids:	
                if dimension.option_id.dimension_id.tipo == 'COLOR':
                    color = dimension.option_id.code 
            if color  and talla and pt.default_code:      
                print color
                print talla
                print pt.default_code
                print pt.default_code + talla + color 
                    
                return pt.default_code + talla + color 

        return ''
product_product()


class product_variant_dimension_type(orm.Model):
    _inherit = "product.variant.dimension.type"  


    _columns = {
        'tipo': fields.selection([('TALLA', 'TALLA'), ('COLOR', 'COLOR')], "Tipo", required=True),
    }

product_variant_dimension_type()   
