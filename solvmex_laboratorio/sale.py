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
import netsvc
from dateutil.relativedelta import relativedelta

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'
    _description= 'Sales Order'
    def _create_pickings_and_procurements(self, cr, uid, order, order_lines, picking_id=False, context=None):
        """Create the required procurements to supply sale order lines, also connecting
        the procurements to appropriate stock moves in order to bring the goods to the
        sale order's requested location.

        If ``picking_id`` is provided, the stock moves will be added to it, otherwise
        a standard outgoing picking will be created to wrap the stock moves, as returned
        by :meth:`~._prepare_order_picking`.

        Modules that wish to customize the procurements or partition the stock moves over
        multiple stock pickings may override this method and call ``super()`` with
        different subsets of ``order_lines`` and/or preset ``picking_id`` values.

        :param browse_record order: sale order to which the order lines belong
        :param list(browse_record) order_lines: sale order line records to procure
        :param int picking_id: optional ID of a stock picking to which the created stock moves
                               will be added. A new picking will be created if ommitted.
        :return: True
        """
        move_obj = self.pool.get('stock.move')
        picking_obj = self.pool.get('stock.picking')
        procurement_obj = self.pool.get('procurement.order')
        proc_ids = []

        for line in order_lines:
            if line.state == 'done':
                continue

            date_planned = self._get_date_planned(cr, uid, order, line, order.date_order, context=context)

            if line.product_id:
                if line.product_id.product_tmpl_id.type in ('product', 'consu'):
                    if not picking_id:
                        picking_id = picking_obj.create(cr, uid, self._prepare_order_picking(cr, uid, order, context=context))
                    move_id = move_obj.create(cr, uid, self._prepare_order_line_move(cr, uid, order, line, picking_id, date_planned, context=context))
                else:
                    # a service has no stock move
                    move_id = False

                proc_id = procurement_obj.create(cr, uid, self._prepare_order_line_procurement(cr, uid, order, line, move_id, date_planned, context=context))
                proc_ids.append(proc_id)
                line.write({'procurement_id': proc_id})
                self.ship_recreate(cr, uid, order, line, move_id, proc_id)

        wf_service = netsvc.LocalService("workflow")
        if picking_id:
            wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)
            #aGREGADO POR OPTIMIT - EN UN MISMO MOVIMIENTO VALIDA SI HAY STOCK.
            print 'picking id!!!'
            print picking_id
            self.pool.get('stock.picking').action_assign(cr, uid, [picking_id,] )
        for proc_id in proc_ids:
            wf_service.trg_validate(uid, 'procurement.order', proc_id, 'button_confirm', cr)

        val = {}
        if order.state == 'shipping_except':
            val['state'] = 'progress'
            val['shipped'] = False

            if (order.order_policy == 'manual'):
                for line in order.order_line:
                    if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                        val['state'] = 'manual'
                        break
        order.write(val)
        return True

    def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
        print 'entro a _prepare_order_line_move'
        print line.product_id.uom_id.id
        print line.product_id.densidad

        if(line.product_uom.id == line.product_id.uom_id.id):
            print 'unidades iguales, sin cambios'
            unidad = line.product_uom.id
            cantidad = line.product_uom_qty
            unidad_uos = line.product_uom.id
            cantidad_uos = line.product_uom_qty
        else:
            print 'unidades distintas!!'
            if (line.product_id.uom_id.name == 'kilo'):
                unidad = line.product_id.uom_id.id
                cantidad = line.product_uom_qty * line.product_id.densidad
                unidad_uos = line.product_uom.id
                cantidad_uos = line.product_uom_qty
            else:
                unidad = line.product_id.uom_id.id
                cantidad = line.product_uom_qty * (1 / line.product_id.densidad)
                unidad_uos = line.product_uom.id
                cantidad_uos = line.product_uom_qty
            print 'original'
            print line.product_uom.id
            print line.product_uom_qty
            print 'modificado'
            print unidad
            print cantidad
        location_id = order.shop_id.warehouse_id.lot_stock_id.id
        output_id = order.shop_id.warehouse_id.lot_output_id.id
        newdate = (datetime.strptime(line.order_id.date_order, '%Y-%m-%d') + relativedelta(hours=12 or 0)).strftime('%Y-%m-%d %H:%M:%S')
        return {
            'name': line.name[:250],
            'picking_id': picking_id,
            'product_id': line.product_id.id,
            #'date': line.order_id.date_confirm, - es unicamente informativo
            'date_expected': newdate,
            'product_qty': cantidad,
            'product_uom': unidad,
            'product_uos_qty': cantidad_uos,
            'product_uos': unidad_uos,
            'product_packaging': line.product_packaging.id,
            'address_id': line.address_allotment_id.id or order.partner_shipping_id.id,
            'location_id': location_id,
            'location_dest_id': output_id,
            'sale_line_id': line.id,
            'tracking_id': False,
            'state': 'draft',
            #'state': 'waiting',
            'segundo_viaje': line.order_id.segundo_viaje,
            'note': line.order_id.comentarios_entrega,
            'company_id': order.company_id.id,
            'forma_envio': line.order_id.forma_envio_texto,
            'tambores': line.tambores,
            'cantidad_tambor': line.cantidad_tambor,
            'price_unit': line.product_id.standard_price or 0.0
        }
    def _prepare_order_line_procurement(self, cr, uid, order, line, move_id, date_planned, context=None):
        print 'entro a _prepare_order_line_procurement'
        print line.product_id.uom_id.id
        print line.product_id.densidad

        if(line.product_uom.id == line.product_id.uom_id.id):
            print 'unidades iguales, sin cambios'
            unidad = line.product_uom.id
            cantidad = line.product_uom_qty
            unidad_uos = line.product_uom.id
            cantidad_uos = line.product_uom_qty
        else:
            print 'unidades distintas!!'
            if (line.product_id.uom_id.name == 'kilo'):
                unidad = line.product_id.uom_id.id
                cantidad = line.product_uom_qty * line.product_id.densidad
                unidad_uos = line.product_uom.id
                cantidad_uos = line.product_uom_qty
            else:
                unidad = line.product_id.uom_id.id
                cantidad = line.product_uom_qty * (1 / line.product_id.densidad)
                unidad_uos = line.product_uom.id
                cantidad_uos = line.product_uom_qty
            print 'original'
            print line.product_uom.id
            print line.product_uom_qty
            print 'modificado'
            print unidad
            print cantidad
        newdate = (datetime.strptime(line.order_id.date_order, '%Y-%m-%d') + relativedelta(hours=12 or 0)).strftime('%Y-%m-%d %H:%M:%S')
        return {
            'name': line.name,
            'origin': order.name,
            'date_planned': newdate,
            'product_id': line.product_id.id,
            'product_qty': cantidad,
            'product_uom': unidad,
            'product_uos_qty': cantidad_uos,
            'product_uos': unidad_uos,
            'location_id': order.shop_id.warehouse_id.lot_stock_id.id,
            'procure_method': line.type,
            'move_id': move_id,
            'company_id': order.company_id.id,
            'note': line.notes
        }

sale_order()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: