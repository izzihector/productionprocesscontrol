# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError
from xlwt import *
from io import BytesIO
import base64
import pdb


class time_sheet_analytic_account(models.TransientModel):
    _name = 'time.sheet.analytic.account'
    _description = 'Time Sheet Analytic Account'

    name = fields.Char(string='Cuenta analítica parte horas')
    exclude_project = fields.Boolean(string='Excluir Proyecto')
    description = fields.Text(
        default='Reporte que busca todas las partes de horas que tengan un proyecto y que las cuentas analítica sean diferentes \n'
                'entre ellos, si se selecciona Excluir Proyecto, las partes de horas que pertenezcan a estos proyectos \n'
                'seleccionados no se tomaran en cuenta\n',
        string='Descripción:', readonly=True)
    projects_ids = fields.Many2many('project.project', string='Proyectos')
    file = fields.Binary(string="Reporte")

    # Project
    @staticmethod
    def time_sheet_analytic_account_excel(project_info_list):
        wb = Workbook(encoding='utf-8')
        row = 0
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_error = easyxf('font: name Calibri; alignment: horizontal left; pattern: pattern solid,'
                             ' fore_colour light_yellow;')
        ws = wb.add_sheet('Cuenta analítica parte horas', cell_overwrite_ok=True)
        ws.write(row, 0, "Proyecto", title)
        ws.write(row, 1, "Cuenta analítica del proyecto", title)
        ws.write(row, 2, "Tarea", title)
        ws.write(row, 3, "Parte de horas", title)
        ws.write(row, 4, "Cuenta analítica de la parte de horas", title)
        for info in project_info_list:
            row += 1
            ws.write(row, 0, info[0], lines)
            ws.write(row, 1, info[1], lines if info[1] != 'No tiene' else lines_error)
            ws.write(row, 2, info[2], lines if info[2] != 'No tiene' else lines_error)
            ws.write(row, 3, info[3], lines if info[3] != 'No tiene' else lines_error)
            ws.write(row, 4, info[4], lines if info[4] != 'No tiene' else lines_error)

        ws.col(0).width += 4000
        ws.col(1).width += 5000
        ws.col(2).width += 8000
        ws.col(3).width += 4000
        ws.col(4).width += 6000

        return wb

    # Button
    def time_sheet_analytic_account_report(self):
        if self.exclude_project and not self.projects_ids:
            raise UserError(_('Must selected a project'))
        aal_obj = self.env['account.analytic.line']
        if self.exclude_project:
            time_sheet = aal_obj.search([('project_id', 'not in', self.projects_ids.ids)])
        else:
            time_sheet = aal_obj.search([])
        if not time_sheet:
            raise UserError (_("Don't found any time sheet"))
        ts_info_list = []
        for ts in time_sheet:
            project = ts.project_id
            if project and project.active and ts.account_id != project.analytic_account_id:
                ts_info_list.append([project.name, project.analytic_account_id.name if project.analytic_account_id else 'No tiene',
                                    ts.task_id.name if ts.task_id else 'No tiene', ts.name if ts.name else 'No tiene',
                                    ts.account_id.name if ts.account_id else 'No tiene'])

        if not ts_info_list:
            raise UserError(_("Don't found any time sheet with analytic account different from his project"))
        excel = self.time_sheet_analytic_account_excel(ts_info_list)

        file_name = 'Cuenta analítica parte horas.xls'
        fp = BytesIO()
        excel.save(fp)
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