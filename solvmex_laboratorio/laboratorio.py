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

class laboratorio_corte(osv.osv):
    def obtener_productos(self,cr,uid,ids,context=None):
        cr.execute('SELECT fecha_corte,id FROM laboratorio_corte WHERE id = ' + str(ids[0]))
        fecha = cr.fetchone()
        #  location_dest_id = 9 selecciona solo los movimientos de salida!
        query = "select id from stock_move where location_dest_id = 9 AND date_expected::timestamp::date = '" + str(fecha[0]) +"' and id not in (SELECT listado_id FROM corte_listado_rel WHERE pedido_id = " + str(fecha[1]) +");"
        cr.execute(query)
        for r in cr.fetchall():
             cr.execute('INSERT INTO corte_listado_rel (pedido_id, listado_id) VALUES (' + str(fecha[1]) + ',' + str(r[0]) + ');')
        return True

    def obtener_productos_atrasados(self,cr,uid,ids,context=None):
        cr.execute('SELECT fecha_corte,id FROM laboratorio_corte WHERE id = ' + str(ids[0]))
        fecha = cr.fetchone()
        #  location_dest_id = 9 selecciona solo los movimientos de salida!
        query = "select id from stock_move where location_dest_id = 9 AND date_expected::timestamp::date =( select DATE 'yesterday') and id not in (SELECT listado_id FROM corte_listado_rel);"
        cr.execute(query)
        for r in cr.fetchall():
             cr.execute('INSERT INTO corte_listado_rel (pedido_id, listado_id) VALUES (' + str(fecha[1]) + ',' + str(r[0]) + ');')
        return True

    _name = 'laboratorio.corte'
    _description= 'Listado de cortes'
    _columns = {
        'name': fields.char('Folio',size=96),
        'fecha_corte':fields.date('Fecha'),
        'pedidos': fields.many2many('stock.move','corte_listado_rel', 'pedido_id','listado_id',   'Pedidos'),
        'comentarios': fields.text('Comentarios'),
   }
    _defaults = {
        'fecha_corte': fields.date.context_today,
        'name': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'laboratorio.corte'),
    }
laboratorio_corte()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: