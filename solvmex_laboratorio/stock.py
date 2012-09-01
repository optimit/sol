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

from osv import osv
from osv import fields
from tools.translate import _
from datetime import *
import time
import pooler
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import math
class stock_picking(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    _description = "Picking List"
    _columns = {
        'date': fields.date('Order Date', help="Date of Order", select=True),
    }
    _order = 'origin desc'
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d')
        }
stock_picking()
class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'
    _description= 'Stock Move'
    _columns = {

        'corte_id': fields.many2many('laboratorio.corte', 'corte_listado_rel', 'listado_id', 'pedido_id', 'Corte'),
        'forma_envio': fields.char('Entrega de mercancia', readonly=True, states={'draft': [('readonly', False)]}, size = 100, help="Forma de entrega para la mercancia"),
        'tambores': fields.char('Envase', help="Tipo de envase para envio.",  size = 100),
        'cantidad_tambor':fields.integer('Cantidad de tambores'),
        'segundo_viaje' : fields.boolean ('Segundo viaje'),
    }
    _order = 'origin desc'

stock_move()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: