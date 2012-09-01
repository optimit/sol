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

class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    _description= 'Sales Order Line'

    def onchange_tambores(self, cr, uid, ids, tambores):
        if tambores:
            TYPES = [
            ('cont_c', 'Contenedores propiedad del cliente'),
            ('cont_s', 'Contenedores propiedad de Solvmex'),
            ('p', 'Pipa'),
            ('pri', 'Porrones incluidos'),
            ('pc', 'Porrones propiedad del cliente'),
            ('s', 'Sacos'),
            ('ta', 'Tambores a cambio'),
            ('ti', 'Tambores incluidos'),
            ('tc', 'Tambores propiedad del cliente'),
            ('tf', 'Tambores facturados con pedido'),
            ('otro', 'Otro'),
            ('vacio', '')]
            dic = eval('dict(%s)'%TYPES)
            tambores = dic[tambores]
            val = {
             'notes': 'Envase: ' + tambores,
            }
        else:
            return {}
        return {'value': val}
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}
        print 'product_id_change'
        lang = lang or context.get('lang',False)
        if not  partner_id:
            raise osv.except_osv(_('No Customer Defined !'), _('You have to select a customer in the sales form !\nPlease set one customer before choosing a product.'))
        warning = {}
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'lang': lang, 'partner_id': partner_id}
        if partner_id:
            lang = partner_obj.browse(cr, uid, partner_id).lang
        context_partner = {'lang': lang, 'partner_id': partner_id}

        if not product:
            return {'value': {'th_weight': 0, 'product_packaging': False,
                'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        if not date_order:
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        res = self.product_packaging_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, packaging, context=context)
        result = res.get('value', {})
        warning_msgs = res.get('warning') and res['warning']['message'] or ''
        product_obj = product_obj.browse(cr, uid, product, context=context)

        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if uos:
            if product_obj.uos_id:
                uos2 = product_uom_obj.browse(cr, uid, uos)
                if product_obj.uos_id.category_id.id != uos2.category_id.id:
                    uos = False
            else:
                uos = False
        if product_obj.description_sale:
            result['notes'] = product_obj.description_sale
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        if update_tax: #The quantity only have changed
            result['delay'] = (product_obj.sale_delay or 0.0)
            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)
            result.update({'type': product_obj.procure_method})

        if not flag:
            result['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
        domain = {}
        if (not uom) and (not uos):
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
                uos_category_id = False
            result['th_weight'] = qty * product_obj.weight
            domain = {'product_uom':
                        [('category_id', '=', product_obj.uom_id.category_id.id)],
                        'product_uos':
                        [('category_id', '=', uos_category_id)]}

        elif uos and not uom: # only happens if uom is False
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
        elif uom: # whether uos is set or not
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
            result['th_weight'] = q * product_obj.weight        # Round the quantity up

        if not uom2:
            uom2 = product_obj.uom_id
        compare_qty = float_compare(product_obj.virtual_available * uom2.factor, qty * product_obj.uom_id.factor, precision_rounding=product_obj.uom_id.rounding)
        if (product_obj.type=='product') and int(compare_qty) == -1 \
          and (product_obj.procure_method=='make_to_stock'):
            warn_msg = _('You plan to sell %.2f %s but you only have %.2f %s available !\nThe real stock is %.2f %s. (without reservations)') % \
                    (qty, uom2 and uom2.name or product_obj.uom_id.name,
                     max(0,product_obj.virtual_available), product_obj.uom_id.name,
                     max(0,product_obj.qty_available), product_obj.uom_id.name)
            warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"
        # get unit price
        print 'product_id_change'
        if not pricelist:
            warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
                    'Please set one before choosing a product.')
            warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
        else:
            producto = self.pool.get('product.product')
            producto = producto.browse(cr, uid, product, context=context)
            product_uom = self.pool.get('product.uom')
            product_uom = product_uom.browse(cr, uid, product_obj.uom_id.id, context=None)
            result['divisa'] = pricelist
            result['tipo_envio'] = 'tambor'
            result['densidad'] = producto.densidad
            price = self.calcula_precio(cr, uid, producto, 1, product_uom,pricelist, context=None)
            print result
            if price is None:
                warn_msg = _("3-Este producto no tiene listas de precio asignadas.")
                warning_msgs += _("Producto incompleto! :") + warn_msg +"\n\n"
                result['price_unit'] = 0
                result['precio_lista'] = 0
                result['product_uom_qty'] = 0
                result['cantidad_tambor'] = 1
            else:
                result.update({'price_unit': price,'precio_lista': price})
        if warning_msgs:
            warning = {
                       'title': _('Configuration Error !'),
                       'message' : warning_msgs
                    }
        return {'value': result, 'domain': domain, 'warning': warning}

    def write(self, cr, uid, ids, vals, context=None):
        if (vals.get('price_unit',False) > 0 and ids):
            cr.execute('SELECT standard_price FROM product_template WHERE id IN (SELECT product_tmpl_id FROM product_product WHERE id IN (SELECT product_id FROM sale_order_line WHERE id = ' + str(ids[0]) +'))')
            costo = cr.fetchone()
            utilidad = vals.get('price_unit',False) - costo[0]
            if costo[0] > 0:
                vals['utilidad'] = utilidad
                vals['utilidad_porcentaje'] = str((utilidad / costo[0])*100) + ' % de utilidad' 
            else:
                vals['utilidad'] = 0
                vals['utilidad_porcentaje'] = 'Costo no establecido' 
        return super(sale_order_line, self).write(cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context=None):
        print 'create nuevooo'
        print vals
        print 'producto nuevooo'
        print vals.get('product_id',False)
        if (vals.get('price_unit',False) > 0 and vals.get('product_id',False)):
            cr.execute('SELECT standard_price from product_template where id in (SELECT product_tmpl_id FROM product_product WHERE id = ' + str(vals.get('product_id',False)) +')')
            costo = cr.fetchone()
            utilidad = vals.get('price_unit',False) - costo[0]
            if costo[0] > 0:
                vals['utilidad'] = utilidad
                vals['utilidad_porcentaje'] = str((utilidad / costo[0])*100) + ' % de utilidad' 
            else:
                vals['utilidad'] = 0
                vals['utilidad_porcentaje'] = 'Costo no establecido' 
        return super(sale_order_line, self).create(cr, uid, vals, context=context)

    def calcular_utilidad(self, cr, uid, nada, price_unit,product_id, context=None):
        result = {}
        if (price_unit > 0 and product_id):
            cr.execute('SELECT standard_price from product_template where id in (SELECT product_tmpl_id FROM product_product WHERE id = ' + str(price_unit) +')')
            costo = cr.fetchone()
            utilidad = product_id - costo[0]
            result['utilidad'] = utilidad
            result['utilidad_porcentaje'] = str((utilidad / costo[0])*100) + ' % de utilidad' 
        else:
            return {}
        return {'value': result}
    def calcula_precio(self, cr, uid, product_id, cantidad, unidad=False, divisa=False, context=None):
            #print 'calcular precio'
            if not unidad:
                return {}
            if unidad:
                print unidad.name
            else: 
                print 'no hay unidad'
            #print 'product_id'
            #print str(product_id.id)
            #print 'cantidad'
            #print str(cantidad)
            cr.execute('select porcentaje, piezas_minimo from product_lista_precio where product_id = ' + str(product_id.id) + ' and  piezas_minimo <=  ' +  str(cantidad) + '   order by piezas_minimo desc')
            lista_asignada = cr.fetchone()
            if lista_asignada:
                print 'Encontro una cantidad menor'
            else :
                cr.execute('select porcentaje, piezas_minimo from product_lista_precio where product_id = ' + str(product_id.id) + ' order by porcentaje desc')
                lista_asignada = cr.fetchone()
                #print 'cantidad muchos'
            #print lista_asignada
            divisa_obj = self.pool.get('product.pricelist')
            divisa_obj = divisa_obj.browse(cr, uid, divisa, context=None)
            #compara la moneda con el costo del producto y la moneda en el pedido
            if cmp(divisa_obj.currency_id.name, product_id.moneda_costo) == 0:
                #monedas de costo y pedido iguales, se toma el costo tal cual. 
                tipo_cambio = 1
            else:
                cr.execute("select name, rate from  res_currency_rate where currency_id in (select id from res_currency where name = 'MXN' ) order by name desc LIMIT 1")
                pesos_tc = cr.fetchone()
                #hay que ver si se convierte de dolares a pesos o de pesos a dolares
                if product_id.moneda_costo == 'MXN':
                    print 'el pedido esta en dolares y el producto en pesos'
                    print divisa_obj.currency_id.rate
                    tipo_cambio = (1 / pesos_tc[1])
                    print tipo_cambio
                else:
                    print 'el pedido esta en pesos y el producto en dolares'
                    tipo_cambio = pesos_tc[1]
            if lista_asignada:
                if unidad.name == 'litro':
                    print 'litro'
                    numero = (((lista_asignada[0] / 100) + 1) * product_id.standard_price) * tipo_cambio
                if unidad.name == 'kilo':
                    print 'kilo'
                    numero = (((lista_asignada[0] / 100) + 1) * product_id.standard_price * ( 1 / product_id.densidad)) * tipo_cambio
            else:
                return None
            print numero
            return numero

    def calcular_cantidad(self, cr, uid, ids, product_id, cantidad_tambor,tambores=False,product_uom_qty=False,product_uom_id=False, divisa=False, context=None): 
        print 'calcular cantidad'
        print 'tipo de envio'
        print tambores
        result = {}
        if not product_id:
            return {}
        producto = self.pool.get('product.product')
        producto = producto.browse(cr, uid, product_id, context=context)
        product_uom = self.pool.get('product.uom')
        product_uom = product_uom.browse(cr, uid, product_uom_id, context=None)
        price = self.calcula_precio(cr, uid, producto, product_uom_qty, product_uom,divisa,context=None)
        print 'precio'
        print price
        if (tambores not in ('cont_c','cont_s','p','pri','pc','s','otro','vacio')):
            if producto.capacidad_lt > 0 or producto.capacidad_kg > 0:
                if product_uom.name == 'litro':
                    result['cantidad_tambor'] = round(product_uom_qty / producto.capacidad_lt)
                    print 'entro a litro'
                else:
                    if producto.capacidad_kg > 0 and product_uom.name == 'kilo': 
                        result['cantidad_tambor'] = round(product_uom_qty / producto.capacidad_kg)
                        print 'entro a kilo'
                    else:
                        print 'No se pudo calcular la cantidad en tambores'
        else:
            result['cantidad_tambor'] = 0
        if price:
            result['price_unit'] = price
            result['precio_lista'] = price
        else:
            return {'warning': {
             'title': _('Error!'),
             'message' : '4-Este producto no tiene listas de precio asignadas.'
              }}
        return {'value': result }


    def calcular_unidad(self, cr, uid, ids, product_id, cantidad_tambor,tipo_envio=False,product_uom_qty=False,product_uom_id=False, divisa=False, context=None): 
        print 'calcular unidad'
        print product_id
        result = {}
        if not product_id:
            return {}
        producto = self.pool.get('product.product')
        producto = producto.browse(cr, uid, product_id, context=context)
        product_uom = self.pool.get('product.uom')
        product_uom = product_uom.browse(cr, uid, product_uom_id, context=None)
        price = self.calcula_precio(cr, uid, producto, product_uom_qty, product_uom,divisa, context=None)
        print product_uom.name
        if product_uom.name == 'litro':
            if product_uom_qty <= 1:
                result['product_uom_qty'] = 1
            else:
                result['product_uom_qty'] = round((1 / producto.densidad) * product_uom_qty)
        if product_uom.name == 'kilo':
            result['product_uom_qty'] = round(producto.densidad * product_uom_qty)
        return {'value': result }

    def calcular_tambores(self, cr, uid, ids, product_id, cantidad_tambor,tipo_envio=False,product_uom_id=False, divisa=False, context=None):
        result = {}
        if not product_id:
            return {'warning': {
                       'title': _('!Error!'),
                       'message' : 'Por favor selecciona un producto.'
                    }}
        if tipo_envio:
            print 'numero en calcular_tambores'
            product = self.pool.get('product.product')
            product = product.browse(cr, uid, product_id, context=context)
            product_uom = self.pool.get('product.uom')
            product_uom = product_uom.browse(cr, uid, product_uom_id, context=None)
            print product_uom.name
            if product_uom.name == 'litro':
                if product.capacidad_lt == 0:
                    return {'warning': {
                    'title': _('Error!'),
                    'message' : '1.2Este producto no tiene capacidad de tambor asignada.'
                        }}
                result['product_uom_qty'] = round(product.capacidad_lt * cantidad_tambor)
                numero = self.calcula_precio(cr, uid, product, product.capacidad_lt * cantidad_tambor, product_uom,divisa)
                print numero
                if numero:
                    result['price_unit'] = numero
                    result['precio_lista'] = numero
                else:
                    return {'warning': {
                    'title': _('Error!'),
                    'message' : '1-Este producto no tiene listas de precio asignadas.'
                        }}
                print 'entro a litro'
            else:
                if product_uom.name == 'kilo':
                    result['product_uom_qty'] = round(product.capacidad_kg * cantidad_tambor)
                    numero = self.calcula_precio(cr, uid, product, product.capacidad_lt * cantidad_tambor,product_uom,divisa)
                    print numero
                    if numero:
                        result['price_unit'] = numero
                        result['precio_lista'] = numero
                    else:
                        return {'warning': {
                        'title': _('Error!'),
                        'message' : '2-Este producto no tiene listas de precio asignadas.'
                            }}
                    print 'entro a kilo'
                else:
                    return {'warning': {
                       'title': _('Error!'),
                       'message' : 'La unidad tiene que ser Kilo o Litro.'
                            }}
        else:
            return {'warning': {
                       'title': _('!Error!'),
                       'message' : 'Por favor selecciona un tipo de envio.'
                    }}
        return {'value': result }

    _columns = {
        'tambores': fields.selection([
            ('cont_c', 'Contenedores propiedad del cliente'),
            ('cont_s', 'Contenedores propiedad de Solvmex'),
            ('p', 'Pipa'),
            ('pri', 'Porrones incluidos'),
            ('pc', 'Porrones propiedad del cliente'),
            ('s', 'Sacos'),
            ('ta', 'Tambores a cambio'),
            ('ti', 'Tambores incluidos'),
            ('tc', 'Tambores propiedad del cliente'),
            ('tf', 'Tambores facturados con pedido'),
            ('otro', 'Otro'),
            ('vacio', '')
            ], 'Forma de entrega', help="Tipo de envase para envio.", select=True),
        'calculadora_tambor': fields.integer('Calculadora de tambores', help="Ayuda a calcular cuantos litros o kilos representan X numero de tambores para un producto."),
        'cantidad_tambor':fields.integer('Cantidad de tambores'),
        'divisa': fields.many2one('product.pricelist', 'Lista de precios'),
        'precio_lista':fields.float('Precio de lista', digits=(5,2)),
        'utilidad':fields.float('Utilidad', digits=(5,2)),
        'utilidad_porcentaje':fields.char('Utilidad porcentaje', size=52),
        'densidad':fields.char('Densidad', size=50),
        'tipo_envio': fields.char('Comentarios',size=20),
   }
    _defaults = {
        'tambores': 'ta',
    }
sale_order_line()

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'
    _description= 'Sales Order'
    def onchange_pricelist_id(self, cr, uid, ids, pricelist_id, order_lines, context={}):
        if (not pricelist_id) or (not order_lines):
            divisa_obj = self.pool.get('product.pricelist')
            divisa_obj = divisa_obj.browse(cr, uid, pricelist_id, context=None)
            if (divisa_obj.currency_id.name == "MXN"):
                val = {
                    'tipo_cambio': str(divisa_obj.currency_id.rate),
                }
            else:
                val = {}
            return {'value': val}
        warning = {
            'title': _('Cambio de moneda!'),
            'message' : _('Debe seleccionar la moneda antes de dar de alta productos, por favor capture nuevamente los articulos.')
        }
        return {'warning': warning}

    def onchange_forma_envio(self, cr, uid, ids, forma_envio):
        if forma_envio:
            TYPES = [
            ('cliente_retira', 'Cliente retira'),
            ('solvmex_propio', 'Envio transporte Solvmex'),
            ('solvmex_rentado', 'Envio transporte externo'),
            ('transportista', 'Flete / transportista'),
            ('directo', 'Directo de proveedor / aduana')]
            dic = eval('dict(%s)'%TYPES)
            forma_envio = dic[forma_envio]
            val = {
                'forma_envio_texto': '' + forma_envio,
                }
        else:
            return {}
        return {'value': val}
    def onchange_partner_address(self, cr, uid, ids, address):
        if address:
            direccion = self.pool.get('res.partner.address').browse(cr, uid, address)
            val = {
                'comentarios_entrega': direccion.entrega,
            }
        else:
            return {}
        return {'value': val}


    def action_wait(self, cr, uid, ids, context=None):
        for o in self.browse(cr, uid, ids):
            if not o.order_line:
                raise osv.except_osv(_('Error !'),_('You cannot confirm a sale order which has no line.'))
            if (o.order_policy == 'manual'):
                self.write(cr, uid, [o.id], {'state': 'manual', 'date_confirm': fields.date.context_today(self, cr, uid, context=context), 'aut_credito': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'p_aut_credito':uid})
            else:
                self.write(cr, uid, [o.id], {'state': 'progress', 'date_confirm': fields.date.context_today(self, cr, uid, context=context)})
            self.pool.get('sale.order.line').button_confirm(cr, uid, [x.id for x in o.order_line])
            message = _("La cotizacion '%s' ha sido aprobada, queda en espera de facturacion.") % (o.name,)
            self.log(cr, uid, o.id, message)
        return True
    def valida_ventas(self, cr, uid, ids, context=None):
        cr.execute("SELECT notas_credito FROM res_partner WHERE id IN (SELECT partner_id FROM sale_order WHERE sale_order.id=%s);",ids)
        nota = cr.fetchone()
        if(nota[0]):
            self.write(cr, uid, ids, {'state':'ventas', 'aut_ventas': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'p_aut_ventas':uid,'notas_dpto_credito':nota[0]}, context=context)
        else:
            self.write(cr, uid, ids, {'state':'ventas', 'aut_ventas': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'p_aut_ventas':uid,'notas_dpto_credito':'Sin notas'}, context=context)

        return True
    def cancela_vendedor(self, cr, uid, ids, context=None):
        print 'Entra a cancela ventas'
        self.write(cr, uid, ids, {'state':'cancel'}, context=context)
        return True

    def cancela_ventas(self, cr, uid, ids, context=None):
        cr.execute("SELECT note FROM sale_order WHERE sale_order.id=%s;",ids)
        nota = cr.fetchone()
        if(nota[0]):
            self.write(cr, uid, ids, {'state':'cancel', 'note': nota[0] + '\n RECHAZADO POR VENTAS - ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),'p_aut_ventas':uid,'aut_ventas': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, context=context)
        else:
            self.write(cr, uid, ids, {'state':'cancel', 'note': 'RECHAZADO POR VENTAS - ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),'p_aut_ventas':uid,'aut_ventas': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, context=context)
        return True
    def cancela_credito(self, cr, uid, ids, context=None):
        cr.execute("SELECT note FROM sale_order WHERE sale_order.id=%s;",ids)
        nota = cr.fetchone()
        if(nota[0]):
            self.write(cr, uid, ids, {'state':'cancel', 'note': nota[0] + '\n RECHAZADO POR CREDITO - ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),'p_aut_credito':uid,'aut_credito': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, context=context)
        else:
            self.write(cr, uid, ids, {'state':'cancel', 'note':'RECHAZADO POR CREDITO - ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) ,'p_aut_credito':uid,'aut_credito': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, context=context)
        return True

    def cambia_condiciones(self, cr, uid, ids,indicaciones, context=None):
        res = ""
        if(indicaciones):
            cr.execute("select sale_condiciones_venta.descripcion from sale_condiciones_venta,sale_order where sale_order.condiciones_id = sale_condiciones_venta.id and sale_order.id=%s;",ids)
            indi = cr.fetchone()
            res = indi[0]
            self.write(cr, uid, ids, {'condiciones_venta':res})
        #return {'value': {'indicaciones' : res }}
        return True

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'tipo_cambio': '',
            'state': 'draft',
            'p_aut_credito': '',
            'p_aut_ventas': '',
            'aut_ventas': False,
            'aut_credito': False,
            'shipped': False,
            'invoice_ids': [],
            'picking_ids': [],
            'date_confirm': False,
            'name': self.pool.get('ir.sequence').get(cr, uid, 'sale.order'),
        })
        return super(sale_order, self).copy(cr, uid, id, default, context=context)

    _columns = {
        'notas_dpto_credito' : fields.text('Notas departamento credito'),
        'segundo_viaje' : fields.boolean ('Segundo viaje',readonly=True, states={'draft': [('readonly', False)]}),
        'encabezado_cotizacion': fields.text('Encabezado cotizacion',help="Texto que aparece al principo de la cotizacion, muy util para personalizar el documento."),
        'condiciones_venta': fields.text('Notas de venta (CLIENTE)*',help="Texto que aparece al final de la cotizacion, muy util para personalizar el documento."),
        'aut_ventas': fields.datetime('Fecha aut. ventas', readonly=True),
        'aut_credito': fields.datetime('Fecha aut. credito', readonly=True),
        'p_aut_ventas': fields.many2one('res.users', 'Persona aut. ventas', select=True, readonly=True),
        'p_aut_credito': fields.many2one('res.users', 'Persona aut. credito', select=True, readonly=True),
        'comentarios_entrega': fields.text('Comentarios entrega', readonly=True, states={'draft': [('readonly', False)]}, help = u'Comentarios que se muestran a trafico'),
        'tipo_cambio':fields.float('Tipo de cambio', digits=(5,3),readonly=True, states={'draft': [('readonly', False)]}),
        'forma_envio_texto': fields.char('Entrega de mercancia texto',size=60),
        'forma_envio': fields.selection([
            ('cliente_retira', 'Cliente retira'),
            ('solvmex_propio', 'Envio transporte Solvmex'),
            ('transportista', 'Flete / transportista'),
            ('solvmex_rentado', 'Envio transporte rentado'),
            ('directo', 'Directo de proveedor / aduana')
            ], 'Entrega de mercancia', readonly=True, states={'draft': [('readonly', False)]}, help="Seleccione la forma de entrega para la mercancia", select=True),
        'state': fields.selection([
            ('draft', 'Cotizacion'),
            ('waiting_date', 'Waiting Schedule'),
            ('confirmado', 'Confirmado'),
            ('ventas', 'Aut. Ventas'),
            ('credito', 'Aut. Credito'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('manual', 'To Invoice'),
            ('progress', 'Pendiente de pago'),
            ('done', 'Pagada'),
            ('cancel', 'Rechazada')
            ], 'Order State', readonly=True, help="Gives the state of the quotation or sales order. \nThe exception state is automatically set when a cancel operation occurs in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception). \nThe 'Waiting Schedule' state is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True)
    }
    _defaults = {
        'encabezado_cotizacion': u'En atencion a su solicitud ponemos a su consideracion la siguiente cotizacion, quedo a sus ordenes para cualquier duda o comentario.',
        'forma_envio': 'solvmex_propio',
    }

sale_order()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: