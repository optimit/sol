# -*- coding: utf-8 -*-
from osv import osv
from osv import fields
from tools.translate import _
import time
import pooler


class hr_employee(osv.osv):
    _name = 'hr.employee'
    _inherit = 'hr.employee'
    _description= 'Empleado'
 
    _columns = {
        #Campos de identificaciones
		'ssnid': fields.char('IMSS', size=32, help='Numero del IMSS'),
        'identification_id': fields.char('IFE', size=32),
        'curp': fields.char('CURP', size=20),
        'rfc': fields.char('RFC', size=20),
        'umf': fields.char('UMF', size=20),
        'cred_infonavit': fields.char('Credito INFONAVIT', size=20),
		
        #Datos Bancarios
		'clabe': fields.char('CLABE', size=18),
        'cuenta_hsbc': fields.char('Cuenta HSBC Nomina', size=20),
		
		#Datos Generales
		'clave':fields.char('Clave',size=10),
		'sdo_dro':fields.float('Salario Diario Integrado', digits=(8,2)),
		'profesion':fields.char('Profesion',size=50),
		'lugar_nacimiento':fields.char('Lugar de Nacimiento',size=50),
		'marital': fields.selection([('union', 'Union Libre'), ('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced')], 'Marital Status'),
		
		#Datos de Contacto
		'mobile_phone': fields.char('Tel. celular empresarial', size=32, readonly=False),
		'telefono_casa': fields.char('Telefono de casa',size=15),
		'telefono_emergencia': fields.char('Telefono para emergencias',size=50),
		'email_personal': fields.char('E-mail personal',size=80),
		'extension': fields.char('Extension',size=10),
		'celular_personal': fields.char('Tel. Celular Personal',size=15),
		
		#Fechas importantes
		'fecha_alta': fields.date('Fecha de Alta'),
		'fecha_baja': fields.date('Fecha de Baja'),
    }

hr_employee()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: