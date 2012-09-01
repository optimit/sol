# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from tools.translate import _
import time
import pooler


class product_laboratorio(osv.osv):
    _name = 'product.laboratorio'
    _description= 'Especificaciones tecnicas para productos'
    _columns = {
        'name': fields.many2one('product.product','Producto', ondelete='cascade'),
        'comentarios':fields.text('Comentarios'),
        #ARCHIVOS DE HOJA TECNICA Y DE SEGURIDAD EN PDF. 
        'hoja_seguridad_nombre':fields.char('Hoja de seguridad',size=150),
        'hoja_tecnica_nombre':fields.char('Carta tecnica',size=150),
        'hoja_seguridad':fields.binary('Hoja de seguridad'),
        'hoja_tecnica':fields.binary('Carta tecnica'),

        #DATOS ETIQUETA TAMBOR - ROMBO DE SEGURIDAD
        'toxicidad':fields.char('Toxicidad',size=150),
        'incendio':fields.char('Incendio',size=150),
        'reactividad':fields.char('Reactividad',size=150),
        'epp':fields.char('E.P.P.',size=150),
        'codigo_etiqueta':fields.char('Codigo',size=150),
        #TEMPORALMENTE - 20 de Agosto 2012
        'lote':fields.char('Lote (temporal)',size=150),

        #CERTIFICADO DE ANALISIS CLINICO
        'analisis':fields.char('Analisis',size=150),
        'analisis_1':fields.char('Analisis',size=150),
        'metodo_1':fields.char('Analisis',size=150),
        'resultado_1':fields.char('Analisis',size=150),
        'especificacion_1':fields.char('Analisis',size=150),
        'analisis_2':fields.char('Analisis',size=150),
        'metodo_2':fields.char('Analisis',size=150),
        'resultado_2':fields.char('Analisis',size=150),
        'especificacion_2':fields.char('Analisis',size=150),
        'analisis_3':fields.char('Analisis',size=150),
        'metodo_3':fields.char('Analisis',size=150),
        'resultado_3':fields.char('Analisis',size=150),
        'especificacion_3':fields.char('Analisis',size=150),
        'analisis_4':fields.char('Analisis',size=150),
        'metodo_4':fields.char('Analisis',size=150),
        'resultado_4':fields.char('Analisis',size=150),
        'especificacion_4':fields.char('Analisis',size=150),
        'analisis_5':fields.char('Analisis',size=150),
        'metodo_5':fields.char('Analisis',size=150),
        'resultado_5':fields.char('Analisis',size=150),
        'especificacion_5':fields.char('Analisis',size=150),
        'analisis_6':fields.char('Analisis',size=150),
        'metodo_6':fields.char('Analisis',size=150),
        'resultado_6':fields.char('Analisis',size=150),
        'especificacion_6':fields.char('Analisis',size=150),
        'analisis_7':fields.char('Analisis',size=150),
        'metodo_7':fields.char('Analisis',size=150),
        'resultado_7':fields.char('Analisis',size=150),
        'especificacion_7':fields.char('Analisis',size=150),
        'analisis_8':fields.char('Analisis',size=150),
        'metodo_8':fields.char('Analisis',size=150),
        'resultado_8':fields.char('Analisis',size=150),
        'especificacion_8':fields.char('Analisis',size=150),
        'analisis_9':fields.char('Analisis',size=150),
        'metodo_9':fields.char('Analisis',size=150),
        'resultado_9':fields.char('Analisis',size=150),
        'especificacion_9':fields.char('Analisis',size=150),
        'analisis_10':fields.char('Analisis',size=150),
        'metodo_10':fields.char('Analisis',size=150),
        'resultado_10':fields.char('Analisis',size=150),
        'especificacion_10':fields.char('Analisis',size=150),
        'analisis_11':fields.char('Analisis',size=150),
        'metodo_11':fields.char('Analisis',size=150),
        'resultado_11':fields.char('Analisis',size=150),
        'especificacion_11':fields.char('Analisis',size=150),
        'analisis_12':fields.char('Analisis',size=150),
        'metodo_12':fields.char('Analisis',size=150),
        'resultado_12':fields.char('Analisis',size=150),
        'especificacion_12':fields.char('Analisis',size=150),
        'analisis_13':fields.char('Analisis',size=150),
        'metodo_13':fields.char('Analisis',size=150),
        'resultado_13':fields.char('Analisis',size=150),
        'especificacion_13':fields.char('Analisis',size=150),
        'analisis_14':fields.char('Analisis',size=150),
        'metodo_14':fields.char('Analisis',size=150),
        'resultado_14':fields.char('Analisis',size=150),
        'especificacion_14':fields.char('Analisis',size=150),
        'analisis_15':fields.char('Analisis',size=150),
        'metodo_15':fields.char('Analisis',size=150),
        'resultado_15':fields.char('Analisis',size=150),
        'especificacion_15':fields.char('Analisis',size=150),
        'analisis_16':fields.char('Analisis',size=150),
        'metodo_16':fields.char('Analisis',size=150),
        'resultado_16':fields.char('Analisis',size=150),
        'especificacion_16':fields.char('Analisis',size=150),
        'analisis_17':fields.char('Analisis',size=150),
        'metodo_17':fields.char('Analisis',size=150),
        'resultado_17':fields.char('Analisis',size=150),
        'especificacion_17':fields.char('Analisis',size=150),
        'observaciones':fields.text('Observaciones'),
        'notas':fields.text('Notas'),
        'aprobado_por':fields.char('Aprobado por',size=150),
    }
product_laboratorio()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: