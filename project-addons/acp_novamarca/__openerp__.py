# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
{
    'name' : 'Mejoras Novamarca',
    'version' : '0.1',
    'author' : 'www.infoacp.es',
    "description": """
    	Mejoras Novamarca
    """,
    'category' : 'Tools',
    'depends' : [
        'purchase','product_variant_multi','point_of_sale','pos_coupons',
    ],
    'data' : [
        'purchase/purchase_view.xml',
        'sale/sale_view.xml',        
        'product/product_view.xml',
        'stock/stock_view.xml',
        'pos/point_of_sale_report.xml',
        'pos/report/report_receipt_regalo.xml',        
        'pos/report/report_receipt_cupon.xml',
        'pos/point_of_sale_view.xml',         
        
        

    ],
    "installable": True,    
}
