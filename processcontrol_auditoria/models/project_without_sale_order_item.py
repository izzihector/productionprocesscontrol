# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError
from xlwt import *
from io import BytesIO
import base64
import pdb


class project_without_sale_order_item(models.TransientModel):
    _name = 'project.without.sale.order.item'
    _description = 'Project Without Sale Order Item'

    name = fields.Char(string='Proyecto sin Pedido de Venta')
    type_report = fields.Selection([
        ('all', 'Todo'),
        ('project', 'Proyectos'),
        ('task', 'Tareas'),
        ('time_sheet', 'Parte de horas')], string='Tipo de Informe', required=True, default='all')
    exclude_project = fields.Boolean(string='Excluir Proyecto')
    description = fields.Text(
        default='Reporte que según el Tipo de Informe que se seleccione realiza diferentes operaciones sobre los Proyectos, \n'
                'Tareas y/o Parte de horas, si seleccionamos excluir proyectos y agregamos proyectos, estos se filtraran en el reporte\n'
                'ya sea en ellos mismos o en las Tareas y Partes de Hora que pertenezcan.\n'
                'Tipo de Informe: \n'
                '               -Proyectos: Devuelve todos los proyectos que no tengan un Pedido de Venta \n'
                '               -Tareas: Devuelve todas las tareas que no tengan un Pedido de Venta \n'
                '               -Parte de horas: Devuelve todas las parte de horas que no tengan un Pedido de Venta \n'
                '               -Todo: Devuelve las 3 opciones anteriores en un solo reporte, sepradas en hojas \n',
        string='Descripción:', readonly=True)
    projects_ids = fields.Many2many('project.project', string='Proyectos')

    file = fields.Binary(string="Reporte")

    # Project
    @staticmethod
    def get_project_ws_header(wb, ws_count):
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        if ws_count:
            ws_name = 'Proyectos sin Pedido de Ventas (' + str(ws_count) + ')'
        else:
            ws_name = 'Proyectos sin Pedido de Ventas'
        ws = wb.add_sheet(ws_name, cell_overwrite_ok=True)
        ws.write(0, 0, "Nombre del proyecto", title)
        ws.write(0, 1, "Cliente", title)
        ws.write(0, 2, "Responsable del proyecto", title)
        ws.write(0, 3, "Tipo de proyecto", title)

        ws.col(0).width += 4000
        ws.col(1).width += 3000
        ws.col(2).width += 4000
        ws.col(3).width += 3000

        return ws

    def project_without_sale_order_item_excel(self, wb, project_info_list):
        ws_count = 0
        row = 0
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_error = easyxf('font: name Calibri; alignment: horizontal left; pattern: pattern solid,'
                             ' fore_colour light_yellow;')
        ws = self.get_project_ws_header(wb, ws_count)
        ws_count = 2
        for info in project_info_list:
            row += 1
            if row == 30000:
                ws = self.get_project_ws_header(wb, ws_count)
                row = 1
                ws_count += 1
            ws.write(row, 0, info[0], lines)
            ws.write(row, 1, info[1], lines if info[1] != 'No tiene' else lines_error)
            ws.write(row, 2, info[2], lines if info[2] != 'No tiene' else lines_error)
            ws.write(row, 3, info[3], lines if info[3] != 'No tiene' else lines_error)

    def get_project_without_sale_order_item(self, wb):
        project_obj = self.env['project.project']
        if self.exclude_project:
            projects = project_obj.search([('sale_line_id', '=', False), ('id', 'not in', self.projects_ids.ids)])
        else:
            projects = project_obj.search([('sale_line_id', '=', False), ('active', '=', True)])
        if self.type_report == 'project' and not projects:
            raise UserError(_('Dont found any Project without Sales Order Item'))
        project_info_list = []
        for pro in projects:
            info = []
            info.append(pro.name)
            info.append(pro.partner_id.name if pro.partner_id else 'No tiene')
            info.append(pro.user_id.name if pro.user_id else 'No tiene')
            info.append(dict(pro._fields['type_project'].selection).get(pro.type_project) if pro.type_project else 'No tiene')
            project_info_list.append(info)
        if project_info_list:
            self.project_without_sale_order_item_excel(wb, project_info_list)

        return project_info_list

    # Task
    @staticmethod
    def get_task_ws_header(wb, ws_count):
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        if ws_count:
            ws_name = 'Tareas sin Pedido de Ventas (' + str(ws_count) + ')'
        else:
            ws_name = 'Tareas sin Pedido de Ventas'
        ws = wb.add_sheet(ws_name, cell_overwrite_ok=True)
        ws.write(0, 0, "Nombre del proyecto", title)
        ws.write(0, 1, "Cliente", title)
        ws.write(0, 2, "Pedido de venta del proyecto", title)
        ws.write(0, 3, "Nombre tarea", title)
        ws.write(0, 4, "Asignado a", title)

        ws.col(0).width += 4000
        ws.col(1).width += 3000
        ws.col(2).width += 5000
        ws.col(3).width += 6000
        ws.col(4).width += 3000

        return ws

    def task_without_sale_order_item_excel(self, wb, task_info_list):
        ws_count = 0
        row = 0
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_error = easyxf('font: name Calibri; alignment: horizontal left; pattern: pattern solid,'
                             ' fore_colour light_yellow;')
        ws = self.get_task_ws_header(wb, ws_count)
        ws_count = 2
        for info in task_info_list:
            row += 1
            if row == 30000:
                ws = self.get_task_ws_header(wb, ws_count)
                row = 1
                ws_count += 1
            ws.write(row, 0, info[0], lines)
            ws.write(row, 1, info[1], lines if info[1] != 'No tiene' else lines_error)
            ws.write(row, 2, info[2], lines if info[2] != 'No tiene' else lines_error)
            ws.write(row, 3, info[3], lines)
            ws.write(row, 4, info[4], lines if info[4] != 'No tiene' else lines_error)

    def get_task_without_sale_order_item(self, wb):
        task_obj = self.env['project.task']
        if self.exclude_project:
            tasks = task_obj.search([('sale_line_id', '=', False), ('project_id', 'not in', self.projects_ids.ids)])
        else:
            tasks = task_obj.search([('sale_line_id', '=', False), ('active', '=', True)])
        if self.type_report == 'task' and not tasks:
            raise UserError(_('Dont found any Tasks without Sales Order Item'))
        task_info_list = []
        for tas in tasks:
            info = []
            project = tas.project_id
            info.append(project.name)
            info.append(tas.partner_id.name if tas.partner_id else 'No tiene')
            info.append(project.sale_line_id.name if project.sale_line_id else 'No tiene')
            info.append(tas.name)
            info.append(tas.user_id.name if tas.user_id else 'No tiene')
            task_info_list.append(info)
        if task_info_list:
            self.task_without_sale_order_item_excel(wb, task_info_list)

        return task_info_list

    # Time Sheet
    @staticmethod
    def get_time_sheet_ws_header(wb, ws_count):
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        if ws_count:
            ws_name = 'Horas Ventas (' + str(ws_count) + ')'
        else:
            ws_name = 'Horas Ventas'
        ws = wb.add_sheet(ws_name, cell_overwrite_ok=True)
        ws.write(0, 0, "Fecha", title)
        ws.write(0, 1, "Proyecto", title)
        ws.write(0, 2, "Tarea", title)
        ws.write(0, 3, "Tiquete del Servicio de Asistencia", title)
        ws.write(0, 4, "Descripción", title)
        ws.write(0, 5, "Cliente del ticket", title)
        ws.write(0, 6, "Tipo facturable", title)

        ws.col(0).width += 3000
        ws.col(1).width += 4000
        ws.col(2).width += 6000
        ws.col(3).width += 8000
        ws.col(4).width += 8000
        ws.col(5).width += 3000
        ws.col(6).width += 3000

        return ws

    def time_sheet_without_sale_order_item_excel(self, wb, time_sheet_info_list):
        ws_count = 0
        row = 0
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_error = easyxf('font: name Calibri; alignment: horizontal left; pattern: pattern solid,'
                             ' fore_colour light_yellow;')
        ws = self.get_time_sheet_ws_header(wb, ws_count)
        ws_count = 2
        for info in time_sheet_info_list:
            row += 1
            if row == 30000:
                break
                ws = self.get_time_sheet_ws_header(wb, ws_count)
                row = 1
                ws_count += 1
            ws.write(row, 0, info[0], lines)
            ws.write(row, 1, info[1], lines if info[1] != 'No tiene' else lines_error)
            ws.write(row, 2, info[2], lines if info[2] != 'No tiene' else lines_error)
            ws.write(row, 3, info[3], lines if info[3] != 'No tiene' else lines_error)
            ws.write(row, 4, info[4], lines)
            ws.write(row, 5, info[5], lines if info[5] != 'No tiene' else lines_error)
            ws.write(row, 6, info[6], lines if info[6] != 'No tiene' else lines_error)

    def get_time_sheet_without_sale_order_item(self, wb):
        aal_obj = self.env['account.analytic.line']
        if self.exclude_project:
            time_sheet = aal_obj.search([('so_line', '=', False), ('project_id', 'not in', self.projects_ids.ids)])
        else:
            time_sheet = aal_obj.search([('so_line', '=', False)])
        if self.type_report == 'time_sheet' and not time_sheet:
            raise UserError(_('Dont found any time_sheets without Sales Order Item'))
        time_sheet_info_list = []
        for ts in time_sheet:
            if (not ts.project_id or ts.project_id.active) and (not ts.task_id or ts.task_id.active):
                info = []
                info.append(ts.date.strftime("%d/%m/%Y"))
                info.append(ts.project_id.name if ts.project_id else 'No tiene')
                info.append(ts.task_id.name if ts.task_id else 'No tiene')
                info.append(ts.helpdesk_ticket_id.name if ts.helpdesk_ticket_id else 'No tiene')
                info.append(ts.name)
                info.append(ts.x_cliente_del_ticket.name if ts.x_cliente_del_ticket else 'No tiene')
                info.append(dict(ts._fields['timesheet_invoice_type'].selection).get(ts.timesheet_invoice_type) if ts.timesheet_invoice_type else 'No tiene')
                time_sheet_info_list.append(info)
        if time_sheet_info_list:
            self.time_sheet_without_sale_order_item_excel(wb, time_sheet_info_list)

        return time_sheet_info_list

    # Button
    def project_without_sale_order_item_report(self):
        if self.exclude_project and not self.projects_ids:
            raise UserError(_('Must selected a project'))
        wb = Workbook(encoding='utf-8')
        if self.type_report in ('all', 'project'):
            file_name = 'Proyectos sin Pedido de Ventas.xls'
            projects = self.get_project_without_sale_order_item(wb)
        if self.type_report in ('all', 'task'):
            file_name = 'Tareas sin Pedido de Ventas.xls'
            tasks = self.get_task_without_sale_order_item(wb)
        if self.type_report in ('all', 'time_sheet'):
            file_name = 'Parte de horas sin Pedido de Ventas.xls'
            time_sheet = self.get_time_sheet_without_sale_order_item(wb)
        if self.type_report == 'all':
            if not projects and not tasks and not time_sheet:
                raise UserError(_('Dont found any Project, Tasks and Time Sheet without Sales Order Item'))
            file_name = 'Todo sin Pedido de Ventas.xls'

        fp = BytesIO()
        wb.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        data_to_save = base64.encodebytes(data)
        self.env.cr.execute("""
                    DELETE
                    FROM descargar_hojas;
                """)
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