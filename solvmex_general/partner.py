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
import time
import pooler


class res_cpostal(osv.osv):

    _description='Codigo postal'
    _name = 'res.cpostal'
    _columns = {
		'codigo': fields.char('Codigo Postal', size=6),
		'name': fields.char('Colonia', size=100),
		'tipo': fields.char('Asentamiento', size=50),
		'municipio': fields.char('Municipio', size=55),
		'estado': fields.char('Estado', size=25),
    }
    _order = 'codigo'

res_cpostal()


class res_partner(osv.osv):

    def autoriza_credito(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'aut_credito'})

    def autoriza_conta(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'activo','active':lambda *a: 1})

    def bloqueo_cliente(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'bloqueado','active': 0})

    def cancela_cliente(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancelado','active': 0})

    def reactivar_cliente(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'borrador','active': 0})

    _name = 'res.partner'
    _inherit = 'res.partner'
    _description= 'Partner'
 
    _columns = {
        'nomcom': fields.char('Nombre comercial', size=200),
        'rfc': fields.char('RFC', size=20, select=1),
        'state': fields.selection([('borrador','Borrador / Inactivo'),
                                   ('aut_credito','Autorizado credito'),
                                   ('activo','Activo'),
                                   ('bloqueado','Bloqueado'),
                                   ('cancelado','Cancelado')], 'Estado', help='Borrador - En este estado no es posible generar un pedido al cliente.'),

        #-----------------------------------Campos para domicilio fiscal---------------------------
        'calle_df': fields.char('Calle', size=200),
        'noexterior_df': fields.char('No. Exterior', size=50),
        'nointerior_df': fields.char('No. Interior', size=50),
        'colonia_df': fields.char('Colonia', size=100),
        'localidad_df': fields.char('Localidad', size=80),
        'municipio_df': fields.char('Municipio', size=80),
        'estado_df': fields.char('Estado', size=80),
        'pais_df': fields.char('Pais', size=50),
        'codigopostal_df': fields.char('Codigo postal', size=10),
        #---------------------------------------------------------------------------------------------
		#-----------------------------------Campos para informacion general---------------------------
        'telefono_1': fields.char('Telefono 1', size=50, select=1),
        'telefono_2': fields.char('Telefono 2', size=50, select=1),
        'email_ventas': fields.char('Email ventas', size=50, select=1),
        'email_facturas': fields.char('Email facturas', size=50, select=1),
        'email_almacen': fields.char('Email almacen', size=50, select=1),
        'fax': fields.char('fax', size=50, select=1),
        'ultima_compra': fields.char('Ultima compra', size=50, select=1),
        'tipo': fields.char('tipo', size=50, select=1),
        'dias': fields.char('Dias de credito', size=50, select=1),
        'revision': fields.char('Revision', size=40, select=1),
        'pagos': fields.char('Pagos', size=40, select=1),
        'clasificacion': fields.char('Clasificacion', size=40, select=1),
        'bloqueado': fields.boolean('Bloqueado'),
        'bloqueado_nota': fields.char('Razon de bloqueo', size=120, select=1),
        'zona': fields.char('Zona Comercial', size=12, select=1),
        'cheques_devueltos': fields.integer('Cheques devueltos'),
        'id_vendedor': fields.integer('ID del vendedor'),
        #---------------------------------------------------------------------------------------------
        #---------Campos para calificar a los clientes por parte de las diferentes áreas--------------
        'calif_ventas': fields.integer('Calificacion de Ventas'),
        'notas_ventas': fields.text('Notas de Ventas'),
        'calif_credito': fields.integer('Calificacion de Credito y Cobranza'),
        'notas_credito': fields.text('Notas de Credito y Cobranza'),
        'calif_trafico': fields.integer('Calificacion de Trafico'),
        'notas_trafico': fields.text('Notas de Trafico'),
        #---------------------------------------------------------------------------------------------
    }
    _defaults = {
        'active': lambda *a: 0,
        'state': 'borrador',
    }
res_partner()


class res_partner_address(osv.osv):
    _name = 'res.partner.address'
    _inherit = 'res.partner.address'
    _description= 'Partner Addresses'
    _columns = {
        'estado': fields.char('Estado',size=30),
        'entrega': fields.text('Entrega', help=u"Comentarios de entrega que son enviados al departamento de trafico"),
        'municipio': fields.char('Municipio',size=120),
    }
	
res_partner_address()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
