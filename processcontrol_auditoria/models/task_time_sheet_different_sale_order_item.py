# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError
from xlwt import *
from io import BytesIO
import base64
import pdb


class task_time_sheet_different_sale_order_item(models.TransientModel):
    _name = 'task.time.sheet.different.sale.order.item'
    _description = 'Task Time Sheet Different Sale Order Item'

    name = fields.Char(string='Diferentes elemento del pedido de venta')
    type_report = fields.Selection([
        ('all', 'Todo'),
        ('task', 'Tareas'),
        ('time_sheet', 'Parte de horas')], string='Tipo de Informe', required=True, default='all')
    exclude_project = fields.Boolean(string='Excluir Proyecto')
    description = fields.Text(
        default='Reporte que según el Tipo de Informe que se seleccione realiza diferentes operaciones sobre las Tareas y/o Parte de horas, \n'
                'si seleccionamos excluir proyectos y agregamos proyectos, no se consideraran las Tareas o Partes de Hora que pertenezcan a estos proyectos.\n'
                'Tipo de Informe: \n'
                '   -Tareas: Devuelve todas las tareas que tengan diferente Pedido de Venta con su proyecto \n'
                '   -Parte de horas: Devuelve todas las parte de horas que tengan diferente Pedido de Venta con su tarea o proyecto\n'
                '   -Todo: Devuelve las 2 opciones anteriores en un solo reporte, sepradas en hojas \n',
        string='Descripción:', readonly=True)
    projects_ids = fields.Many2many('project.project', string='Proyectos')

    file = fields.Binary(string="Reporte")

    # Task
    @staticmethod
    def task_different_sale_order_item_excel(wb, task_info_list):
        row = 0
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_error = easyxf('font: name Calibri; alignment: horizontal left; pattern: pattern solid,'
                             ' fore_colour light_yellow;')
        ws = wb.add_sheet('Tareas diferentes Pedido de Venta', cell_overwrite_ok=True)
        ws.write(row, 0, "Nombre del proyecto", title)
        ws.write(row, 1, "Cliente", title)
        ws.write(row, 2, "Pedido de venta del proyecto", title)
        ws.write(row, 3, "Nombre tarea", title)
        ws.write(row, 4, "Asignado a", title)
        for info in task_info_list:
            row += 1
            ws.write(row, 0, info[0], lines)
            ws.write(row, 1, info[1], lines if info[1] != 'No tiene' else lines_error)
            ws.write(row, 2, info[2], lines if info[2] != 'No tiene' else lines_error)
            ws.write(row, 3, info[3], lines)
            ws.write(row, 4, info[4], lines if info[4] != 'No tiene' else lines_error)

        ws.col(0).width += 4000
        ws.col(1).width += 3000
        ws.col(2).width += 5000
        ws.col(3).width += 6000
        ws.col(4).width += 3000

    def get_task_different_sale_order_item(self, wb):
        task_obj = self.env['project.task']
        if self.exclude_project:
            tasks = task_obj.search([('project_id', 'not in', self.projects_ids.ids)])
        else:
            tasks = task_obj.search([('active', '=', True)])
        if self.type_report == 'task' and not tasks:
            raise UserError(_('Dont found any Tasks without Sales Order Item'))
        task_info_list = []
        for tas in tasks:
            if tas.project_id and tas.sale_line_id != tas.project_id.sale_line_id:
                info = []
                project = tas.project_id
                info.append(project.name)
                info.append(tas.partner_id.name if tas.partner_id else 'No tiene')
                info.append(project.sale_line_id.name if project.sale_line_id else 'No tiene')
                info.append(tas.name)
                info.append(tas.user_id.name if tas.user_id else 'No tiene')
                task_info_list.append(info)
        if task_info_list:
            self.task_different_sale_order_item_excel(wb, task_info_list)

        return task_info_list

    # Time Sheet
    @staticmethod
    def time_sheet_different_sale_order_item_excel(wb, time_sheet_info_list):
        row = 0
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_error = easyxf('font: name Calibri; alignment: horizontal left; pattern: pattern solid,'
                             ' fore_colour light_yellow;')
        ws = wb.add_sheet('Parte de Horas diferentes Pedido de Ventas', cell_overwrite_ok=True)
        ws.write(row, 0, "Fecha", title)
        ws.write(row, 1, "Proyecto", title)
        ws.write(row, 2, "Tarea", title)
        ws.write(row, 3, "Tiquete del Servicio de Asistencia", title)
        ws.write(row, 4, "Descripción", title)
        ws.write(row, 5, "Cliente del ticket", title)
        ws.write(row, 6, "Tipo facturable", title)
        ws.write(row, 7, "Diferencia", title)
        for info in time_sheet_info_list:
            row += 1
            ws.write(row, 0, info[0], lines)
            ws.write(row, 1, info[1], lines if info[1] != 'No tiene' else lines_error)
            ws.write(row, 2, info[2], lines if info[2] != 'No tiene' else lines_error)
            ws.write(row, 3, info[3], lines if info[3] != 'No tiene' else lines_error)
            ws.write(row, 4, info[4], lines)
            ws.write(row, 5, info[5], lines if info[5] != 'No tiene' else lines_error)
            ws.write(row, 6, info[6], lines if info[6] != 'No tiene' else lines_error)
            ws.write(row, 7, info[7], lines)

        ws.col(0).width += 3000
        ws.col(1).width += 4000
        ws.col(2).width += 6000
        ws.col(3).width += 8000
        ws.col(4).width += 8000
        ws.col(5).width += 3000
        ws.col(6).width += 3000
        ws.col(7).width += 3000

    def get_time_sheet_different_sale_order_item(self, wb):
        aal_obj = self.env['account.analytic.line']
        if self.exclude_project:
            time_sheet = aal_obj.search([('project_id', 'not in', self.projects_ids.ids)])
        else:
            time_sheet = aal_obj.search([])
        if self.type_report == 'time_sheet' and not time_sheet:
            raise UserError(_('Dont found any time_sheets without Sales Order Item'))
        time_sheet_info_list = []
        for ts in time_sheet:
            if ts.task_id and ts.project_id and ts.task_id.active and ts.project_id.active and (ts.so_line != ts.task_id.sale_line_id or ts.so_line != ts.task_id.sale_line_id):
                info = []
                info.append(ts.date.strftime("%d/%m/%Y"))
                info.append(ts.project_id.name if ts.project_id else 'No tiene')
                info.append(ts.task_id.name if ts.task_id else 'No tiene')
                info.append(ts.helpdesk_ticket_id.name if ts.helpdesk_ticket_id else 'No tiene')
                info.append(ts.name)
                info.append(ts.x_cliente_del_ticket.name if ts.x_cliente_del_ticket else 'No tiene')
                info.append(dict(ts._fields['timesheet_invoice_type'].selection).get(ts.timesheet_invoice_type) if ts.timesheet_invoice_type else 'No tiene')
                info.append('Diferencia con Tarea' if ts.task_id and ts.so_line != ts.task_id.sale_line_id else 'Diferencia con Proyecto')
                time_sheet_info_list.append(info)
        if time_sheet_info_list:
            self.time_sheet_different_sale_order_item_excel(wb, time_sheet_info_list)

        return time_sheet_info_list

    # Button
    def task_time_sheet_different_sale_order_item_report(self):
        if self.exclude_project and not self.projects_ids:
            raise UserError(_('Must selected a project'))
        wb = Workbook(encoding='utf-8')
        if self.type_report in ('all', 'task'):
            file_name = 'Tareas con diferentes elemento del pedido de venta.xls'
            tasks = self.get_task_different_sale_order_item(wb)
        if self.type_report in ('all', 'time_sheet'):
            file_name = 'Parte de horas con diferentes elemento del pedido de venta.xls'
            time_sheet = self.get_time_sheet_different_sale_order_item(wb)
        if self.type_report == 'all':
            if not tasks and not time_sheet:
                raise UserError(_('Dont found any Tasks or Time Sheet without Sales Order Item'))
            file_name = 'Todo con diferentes elemento del pedido de venta.xls'

        fp = BytesIO()
        wb.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
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