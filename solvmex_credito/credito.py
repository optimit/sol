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

class credito_programacion_cobros(osv.osv):
    def onchange_name(self, cr, uid, ids, factura):
        v = {}
        print 'cambio de factura'
        print factura
        if factura:
            datos_factura = self.pool.get('account.invoice').browse(cr, uid, factura)
            print datos_factura
            v['pedido'] = datos_factura.origin
            v['cliente_id'] = datos_factura.partner_id.id
            v['codigo_cliente'] = datos_factura.partner_id.ref
            v['importe'] = datos_factura.amount_total
            v['divisa'] = datos_factura.currency_id.id
            v['fecha_vencimiento'] = datos_factura.date_due
            v['fecha_pago'] = datos_factura.date_due
        return {'value': v}

    _name = 'credito.programacion_cobros'
    _description= 'Programacion de cobros'
    _columns = {
        'fecha_pago':fields.date('Fecha programada de pago'),
        'fecha_vencimiento':fields.date('Fecha de vencimiento'),
        'name': fields.many2one('account.invoice', 'Factura', domain="[('type','=','out_invoice')]"),
        'pedido': fields.char( 'Pedido original',size=20),
        'divisa': fields.many2one('res.currency', 'Divisa'),
        'cobrador_id':fields.many2one('credito.cobrador','Ruta / cobrador asignado'),
        'cliente_id':fields.many2one('res.partner','Cliente'),
        'codigo_cliente' : fields.char('Cuenta',size=20),
        'importe' : fields.float('Saldo pendiente',digits=(16, 2)),
        'motivo_visita' : fields.selection([
            ('revision', 'Revision'),
            ('cobro', 'Cobranza'),
        ], 'Motivo de visita', help='Especifica si es una factura en revision o para cobranza'),
        'dias_atraso' : fields.char('Dias de retraso',size=20),
        'comentarios': fields.text('Comentarios'),
   }
credito_programacion_cobros()

class credito_cobrador(osv.osv):
    _name = 'credito.cobrador'
    _description= 'Lista de cobradores'
    _columns = {
        'name':fields.char('Nombre', size=52),
        'ruta':fields.char('Ruta asignada', size=50),
        'comentarios': fields.text('Comentarios'),
   }
credito_cobrador()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: