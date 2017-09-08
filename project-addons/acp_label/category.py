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

from openerp import tools
from openerp.osv import fields,osv
import time
from mx import DateTime
from datetime import datetime

class category(osv.osv):
    _inherit = 'product.category'
 

    _columns = {
        'enviaradjuntopc': fields.boolean('Enviar Adjuntos de productos en el pedido de compra',
                                         help="Si esta marcado, los adjuntos de los productos de esta categoria se enviaran en el email del pedido de compras"),
        }                                              

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
