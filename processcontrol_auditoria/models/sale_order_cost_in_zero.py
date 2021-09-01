# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError
from xlwt import *
from io import BytesIO
import base64
from datetime import date
from dateutil.relativedelta import relativedelta


class sale_order_cost_zero(models.TransientModel):
    _name = 'sale.order.cost.zero'
    _description = 'Sale Order Cost Zero'

    def _get_default_start_date(self):
        today = date.today()
        return today.replace(day=1)

    def _get_default_stop_date(self):
        return date.today()

    name = fields.Char(string='Pedido de venta con coste en 0')
    start = fields.Date(string='Desde', required=True, default=_get_default_start_date)
    stop = fields.Date(string='Hasta', required=True, default=_get_default_stop_date)
    exclude_category = fields.Boolean(string='Excluir categorias de producto')
    category_ids = fields.Many2many('product.category', string='Categoria de Producto')
    description = fields.Text(
        default='Devuelve todas las lineas de los pedidos de ventas que no tengan un costo y la fecha de confirmación este \n'
                'dentro de los rangos de fechas ingresados, si clickeamos la opcion de Excluir categorias de producto\n'
                'esta no tomara en cuenta todas las lineas de pedido de venta que tengan un producto de esta categoria.\n',
        string='Descripción:', readonly=True)
    file = fields.Binary(string="Reporte")

    @staticmethod
    def sale_order_cost_in_zero_excel(sales_info_list):
        wb = Workbook(encoding='utf-8')
        row = 0
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_number = easyxf('font: name Calibri; alignment: horizontal right',
                              num_format_str='#,##0.000;-#,##0.000;')
        if sales_info_list:
            ws = wb.add_sheet('Pedido de venta de subscripcion', cell_overwrite_ok=True)
            ws.write(row, 0, "Pedido de Venta", title)
            ws.write(row, 1, "Cliente", title)
            ws.write(row, 2, "Fecha del Pedido", title)
            ws.write(row, 3, "Producto", title)
            ws.write(row, 4, "Categoria", title)
            ws.write(row, 5, "Precio", title)
            ws.write(row, 6, "Importe", title)
            for info in sales_info_list:
                row += 1
                ws.write(row, 0, info[0], lines)
                ws.write(row, 1, info[1], lines)
                ws.write(row, 2, info[2], lines)
                ws.write(row, 3, info[3], lines)
                ws.write(row, 4, info[4], lines)
                ws.write(row, 5, info[5], lines_number)
                ws.write(row, 6, info[6], lines_number)

            ws.col(0).width += 1700
            ws.col(1).width += 725
            ws.col(2).width += 2000
            ws.col(3).width += 7000
            ws.col(4).width += 3000
            ws.col(5).width += 725
            ws.col(6).width += 725

        return wb

    def sale_order_cost_in_zero_report(self):
        if self.exclude_category and not self.category_ids:
            raise UserError(_('Must selected a product category'))
        sale_order_ids = self.env['sale.order'].search([('date_order', '>=', self.start), ('date_order', '<=', self.stop), ('state', 'not in', ('draft', 'sent', 'cancel'))])
        if not sale_order_ids:
            raise UserError(_('Dont found any Sale Order in that range of dates'))
        sales_info_list = []
        for so in sale_order_ids:
            for sol in so.order_line:
                if sol.product_id:
                    if not sol.purchase_price:
                        if self.exclude_category:
                            if sol.product_id.categ_id.id not in self.category_ids.ids:
                                sales_info_list.append([so.name, so.partner_id.name, so.date_order.strftime("%d/%m/%Y"), sol.product_id.name, sol.product_id.categ_id.name, sol.price_unit, sol.price_subtotal])
                        else:
                            sales_info_list.append([so.name, so.partner_id.name, so.date_order.strftime("%d/%m/%Y"), sol.product_id.name, sol.product_id.categ_id.name, sol.price_unit, sol.price_subtotal])
        if not sales_info_list:
            raise UserError(_('Dont found any Sale Order with lines without cost in that range of dates'))
        excel = self.sale_order_cost_in_zero_excel(sales_info_list)

        fp = BytesIO()
        excel.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        file_name = 'Pedido de venta coste en 0.xls'
        data_to_save = base64.encodebytes(data)
        wiz_id = self.env['descargar.hojas'].create({'archivo_nombre': file_name, 'archivo_contenido': data_to_save})
        return {
            'name': "Descargar Archivo",
            'type': 'ir.actions.act_window',
            'res_model': 'descargar.hojas',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz_id.id,
            'views': [(False, 'form')],
            'target': 'new',
        }