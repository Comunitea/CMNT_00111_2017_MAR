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


{
    'name': 'IWAN21 Product Label in Purchases',
    'version': '1.0.1',
    'category': 'Label printing',
    'sequence': 6,
    'summary': 'Impresion etiquetas en pedidos',
    'description': """

    """,
    'author': 'www.iwan21.net',
    'images': [],
    'depends': ['purchase'],
    'data': [
        'view.xml',
        #'report/product_label.xml',        
        'report/product_label_purchases.xsl',                
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'application': False,
    'js': [
    ],
    'css': [
    ],
    'qweb': [],
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
