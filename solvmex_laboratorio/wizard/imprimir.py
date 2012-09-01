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
import netsvc

class imprimir_corte_impresion(osv.osv_memory):
    _name = "laboratorio.corte.impresion"
    _description = "Impresion y envio de cortes"
    def imprimir_corte(self,cr,uid,ids,context=None):
        print context['active_ids']
        url = 'http://192.168.1.5/reportes/corte_laboratorio.php?documentos=' + str(context['active_ids'])
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new'
        }
    def imprimir_corte_detalle(self,cr,uid,ids,context=None):
        print context['active_ids']
        url = 'http://192.168.1.5/reportes/corte_laboratorio_resumen.php?documentos=' + str(context['active_ids'])
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new'
        }
    def imprimir_certificados(self,cr,uid,ids,context=None):
        print context['active_ids']
        url = 'http://192.168.1.5/reportes/lista_certificados.php?documentos=' + str(context['active_ids'])
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new'
        }
    def imprimir_etiquetas(self,cr,uid,ids,context=None):
        print context['active_ids']
        url = 'http://192.168.1.5/reportes/lista_etiquetas.php?documentos=' + str(context['active_ids'])
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new'
        }
imprimir_corte_impresion()