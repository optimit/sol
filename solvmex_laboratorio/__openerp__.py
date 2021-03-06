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
	"name" : "Solvmex Personalizacion - Laboratorio",
	"version" : "1",
	"description" : "Solvmex - Agrega el menu de programacion de cobros para el area de laboratorio",
	"author" : "OPTIMIT S.A. de C.V.",
	"website" : "http://www.optimit.com.mx",
	"depends" : ['base','account','document','sale'], 
	"category" : "Others",
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : ['view/producto.xml','secuencia.xml','view/product_view_solvmex.xml','view/stock_move_view.xml','wizard/imprimir.xml'],
	"active": False,
	"installable": True,
}

