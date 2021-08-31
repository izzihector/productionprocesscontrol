# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError
from xlwt import *
from io import BytesIO
import base64
from datetime import date
from dateutil.relativedelta import relativedelta


class SaleOrderLineWithoutProjectReport(models.TransientModel):
    _name = 'sale.order.line.without.project.report'
    _description = 'Sale Order Line Without Project Report'

    def _get_default_start_date(self):
        today = date.today()
        return today.replace(day=1)

    def _get_default_stop_date(self):
        return date.today()

    name = fields.Char(string='Pedidos de venta sin proyecto')
    start = fields.Date(string='Desde', required=True, default=_get_default_start_date)
    stop = fields.Date(string='Hasta', required=True, default=_get_default_stop_date)
    description = fields.Text(
        default='Reporte que devuelve todas las lineas de venta que no tengan un proyecto relacionado,\n'
                'el producto seleccionado sea de tipo Servicio y este dentro del rango de fechas ingresado\n',
        string='Descripción:', readonly=True)
    file = fields.Binary(string="Report")

    @staticmethod
    def sol_without_project_excel(sales_info_list):
        wb = Workbook(encoding='utf-8')
        row = 0
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_number = easyxf('font: name Calibri; alignment: horizontal right',
                              num_format_str='#,##0.000;-#,##0.000;')
        ws = wb.add_sheet('Pedidos de venta sin proyecto', cell_overwrite_ok=True)
        ws.write(row, 0, "Descripción", title)
        ws.write(row, 1, "Nombre", title)
        ws.write(row, 2, "Producto", title)
        ws.write(row, 3, "Fecha de confirmación", title)
        ws.write(row, 4, "Importe", title)
        for info in sales_info_list:
            row += 1
            ws.write(row, 0, info[0], lines)
            ws.write(row, 1, info[1], lines)
            ws.write(row, 2, info[2], lines)
            ws.write(row, 3, info[3], lines)
            ws.write(row, 4, info[4], lines_number)

        ws.col(0).width += 725
        ws.col(1).width += 725
        ws.col(2).width += 725
        ws.col(3).width += 725
        ws.col(4).width += 725

        return wb

    def sol_without_project_report(self):
        sale_order_ids = self.env['sale.order'].search([('date_order', '>=', self.start), ('date_order', '<=', self.stop),('state', 'not in', ('draft', 'sent', 'cancel'))])
        if not sale_order_ids:
            raise UserError(_('Dont found any Sale Order Line in that range of dates'))
        sol_without_project = self.env['sale.order.line'].search([('order_id', 'in', sale_order_ids.ids), ('project_id', '=', False)])
        if not sol_without_project:
            raise UserError(_('Dont found any Sale Order Line without project in that range of dates'))
        sol_info_list = []
        for sol in sol_without_project:
            info = []
            if sol.product_id and sol.product_id.type == 'service':
                info.append(sol.name)
                info.append(sol.order_id.name)
                info.append(sol.product_id.name)
                info.append(sol.order_id.date_order.strftime("%d/%m/%Y"))
                info.append(sol.price_subtotal)
                sol_info_list.append(info)
        if not sol_info_list:
            raise UserError(_('Dont found any Sale Order Line without project'
                              ' with a service type product in that range of dates'))
        excel = self.sol_without_project_excel(sol_info_list)

        fp = BytesIO()
        excel.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        file_name = 'Pedidos de venta sin proyecto.xls'
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