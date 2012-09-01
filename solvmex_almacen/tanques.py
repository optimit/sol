# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from tools.translate import _
import time
import pooler


class stock_tanque_medida(osv.osv):
    _name = 'stock.tanque.medida'
    _description= 'Relacion altura-volumen de contenido de tanques'
    _columns = {
		'tanque_id': fields.many2one('stock.tanque', 'Tanque estacionario', required=True, ondelete='cascade'),
		'altura': fields.float('Centimetros de altura', digits=(5, 2)),
        'volumen': fields.float('Volumen en litros', digits=(10, 2)),
    }

stock_tanque_medida()

class stock_tanque(osv.osv):
	_name='stock.tanque'
	_descripcion='Tanque estacionarios de almacen'
	_columns={
		'name': fields.char('Nombre del tanque', size=32),
	}

stock_tanque()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: