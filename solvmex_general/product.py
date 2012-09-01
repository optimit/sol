# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from tools.translate import _
import time
import pooler

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    _description= 'Productos'
#UPDATE product_product SET capacidad_kg = round(capacidad_kg,0);
    def capacidad_kg(self, cr, uid, ids, densidad, capacidad_lt, context=None):
        print 'capacidad_kg'
        result = {}
        result['capacidad_kg'] = round(densidad * capacidad_lt)
        print result
        return {'value': result }

    _columns = {
	
        'densidad':fields.float('Densidad', digits=(4,5)),
		'costo_reposicion':fields.float('Costo de reposicion', digits=(5,2), help="Costo actual en el mercado para el producto (INFORMATIVO)."),
		'capacidad_lt':fields.float('Capacidad tambor litros', digits=(5,0)),
		'capacidad_kg':fields.float('Capacidad tambor kilos', digits=(5,0)),
		'escala_precio_ids':fields.one2many('product.lista_precio','product_id','Lista de precios relacionada'),
        'moneda_costo':fields.selection([('USD','Dolares'),
                                      ('MXN','Pesos')],'Moneda para costo', help="Se utiliza en el calculo del precio de venta de acuerdo a las listas de precio." ,required=1),
    }

product_product ()

class product_lista_precio(osv.osv):
    _name = 'product.lista_precio'
    _description= 'Lista de precios para productos'


    def nombre(self, cr, uid, ids, name,piezas_minimo,porcentaje, context=None):
        result = {}
        result['name'] = str(piezas_minimo) + ' piezas con % de: ' + str(porcentaje)
        return {'value': result }

    _columns = {
        'product_id': fields.many2one('product.product','Producto', ondelete='cascade'),
        'name':fields.char('Nombre', size=60),
		'piezas_minimo':fields.float('Minimo de piezas', digits=(5,2)),
		'porcentaje':fields.float('Porcentaje sobre costo base', digits=(5,2)),
        
    }

product_lista_precio ()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: