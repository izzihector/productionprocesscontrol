# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError
from xlwt import *
from io import BytesIO
import base64
from datetime import date
from dateutil.relativedelta import relativedelta

EXPENSE_TYPE = ['Dieta', 'Dieta Sujeta', 'Km Desplazo']
EXPENSES_DIC = {'Dieta Sujeta': 3,
                'Plus Productividad': 4,
                'Dieta': 5,
                'Km Desplazo Sujeta': 6,
                'Km Desplazo': 7}
MAP_MESES = {1: 'Enero',
             2: 'Febrero',
             3: 'Marzo',
             4: 'Abril',
             5: 'Mayo',
             6: 'Junio',
             7: 'Julio',
             8: 'Agosto',
             9: 'Setiembre',
             10: 'Octubre',
             11: 'Noviembre',
             12: 'Diciembre'}


class PCSageReport(models.TransientModel):
    _name = 'pc.sage.report'
    _description = 'Sage Excel Report'

    def _get_default_start_date(self):
        today = date.today()
        return today.replace(day=1)

    def _get_default_stop_date(self):
        return date.today()

    name = fields.Char(string='SAGE')
    start = fields.Date(string='Desde', required=True, default=_get_default_start_date)
    stop = fields.Date(string='Hasta', required=True, default=_get_default_stop_date)
    file = fields.Binary(string="Report")

    @staticmethod
    def sage_excel(dic_sorted, dates, company, stop):
        wb = Workbook(encoding='utf-8')
        row = 6
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left; pattern: pattern solid, fore_color dark_teal;')
        importe = easyxf('font: name Calibri, bold True; alignment: horizontal center; pattern: pattern solid, fore_color dark_teal;')
        lines_green = easyxf('font: name Calibri; alignment: horizontal left; pattern: pattern solid, fore_color lime;')
        lines_0 = easyxf('font: name Calibri; alignment: horizontal right; borders: right thin, top thin, left thin, bottom thin;')
        lines_number = easyxf('font: name Calibri; alignment: horizontal right; borders: right thin, top thin, left thin, bottom thin;',
                              num_format_str='#,##0.00;-#,##0.00;')
        ws = wb.add_sheet('SAGE', cell_overwrite_ok=True)
        ws.write(0, 0, "Empresa:", title)
        ws.write(1, 0, "", title)
        ws.write(2, 0, "Proceso:", title)
        ws.write(3, 0, "Período:", title)
        ws.write_merge(0, 0, 1, 2, company, lines_green)
        ws.write_merge(1, 1, 1, 2, '', lines_green)
        ws.write_merge(2, 2, 1, 2, 'Mes normal', lines_green)
        ws.write_merge(3, 3, 1, 2, MAP_MESES[stop.month] + ' ' + str(stop.year), lines_green)
        ws.write_merge(5, 5, 0, 2, "Empleados", title)
        ws.write(5, 3, "DIETAS SUJETA", title)
        ws.write(5, 4, "PLUS PRODUCCIÓN", title)
        ws.write(5, 5, "DIETAS", title)
        ws.write(5, 6, "KILOMETROS DESPLAZO SUJETO", title)
        ws.write(5, 7, "KILOMETROS DESPLAZO", title)
        ws.write(6, 0, "Código", title)
        ws.write(6, 1, "Nombre", title)
        ws.write(6, 2, "Fecha Alta", title)
        ws.write(6, 3, "Importe", importe)
        ws.write(6, 4, "Importe", importe)
        ws.write(6, 5, "Importe", importe)
        ws.write(6, 6, "Importe", importe)
        ws.write(6, 7, "Importe", importe)
        for code in dic_sorted:
            row += 1
            ws.write(row, 0, code[0], lines_green)
            info = code[1]
            ws.write(row, 1, info[0], lines_green)
            ws.write(row, 2, (info[1].strftime("%d/%m/%Y") if info[1] else ''), lines_green)
            ws.write(row, 3, 0, lines_0)
            ws.write(row, 4, 0, lines_0)
            ws.write(row, 5, 0, lines_0)
            ws.write(row, 6, 0, lines_0)
            ws.write(row, 7, 0, lines_0)
            for expenses in info[2]:
                ws.write(row, EXPENSES_DIC[expenses], info[2][expenses], lines_number)

        ws.col(0).width += 400
        ws.col(1).width += 2000
        ws.col(2).width += 400
        ws.col(3).width += 1400
        ws.col(4).width += 2500
        ws.col(5).width += 1200
        ws.col(6).width += 5000
        ws.col(7).width += 3200

        return wb

    def sage_report(self):
        company = self.env['res.company'].browse(1).name
        expense_type_obj = self.env['pc.hr.expense.type']
        expense_type_ids = expense_type_obj.search([('name', 'in', EXPENSE_TYPE)])
        expense_obj = self.env['hr.expense']
        expense_ids = expense_obj.search([('date', '>=', self.start), ('date', '<=', self.stop), ('expense_type_id', 'in', expense_type_ids.ids)])
        plus_productividad_obj = self.env['pc.plus.productividad']
        plus_productividad_ids = plus_productividad_obj.search([('date', '>=', self.start), ('date', '<=', self.stop)])
        if not expense_ids and not plus_productividad_ids:
            raise UserError(_('No se encontraron datos entre ese rango de fechas'))
        dic_info = {}
        for pp in plus_productividad_ids:
            if not pp.employee_id.cod_employee:
                raise UserError(_('El empleado %s no tiene codigo de empleado' % pp.employee_id.name))
            if pp.employee_id.cod_employee in dic_info:
                dic_info[pp.employee_id.cod_employee][2]['Plus Productividad'] += pp.amount
            else:
                dic_info[pp.employee_id.cod_employee] = [pp.employee_id.name, pp.employee_id.discharge_date, {'Plus Productividad': pp.amount}]
        for exp in expense_ids:
            if not exp.employee_id.cod_employee:
                raise UserError(_('El empleado %s no tiene codigo de empleado' % exp.employee_id.name))
            if exp.expense_type_id.name == 'Km Desplazo':
                km = exp.quantity
                amount_exento = km * 0.19
                amount_sujeto = exp.total_amount - amount_exento if (exp.total_amount - amount_exento) > 0 else 0
                if exp.employee_id.cod_employee in dic_info:
                    if exp.expense_type_id.name in dic_info[exp.employee_id.cod_employee][2]:
                        dic_info[exp.employee_id.cod_employee][2][exp.expense_type_id.name] += amount_exento
                        dic_info[exp.employee_id.cod_employee][2]['Km Desplazo Sujeta'] += amount_sujeto
                    else:
                        dic_info[exp.employee_id.cod_employee][2][exp.expense_type_id.name] = amount_exento
                        dic_info[exp.employee_id.cod_employee][2]['Km Desplazo Sujeta'] = amount_sujeto
                else:
                    dic_info[exp.employee_id.cod_employee] = [exp.employee_id.name, exp.employee_id.discharge_date,
                                                              {exp.expense_type_id.name: amount_exento,
                                                               'Km Desplazo Sujeta': amount_sujeto}]
            else:
                if exp.employee_id.cod_employee in dic_info:
                    if exp.expense_type_id.name in dic_info[exp.employee_id.cod_employee][2]:
                        dic_info[exp.employee_id.cod_employee][2][exp.expense_type_id.name] += exp.total_amount
                    else:
                        dic_info[exp.employee_id.cod_employee][2][exp.expense_type_id.name] = exp.total_amount
                else:
                    dic_info[exp.employee_id.cod_employee] = [exp.employee_id.name, exp.employee_id.discharge_date, {exp.expense_type_id.name: exp.total_amount}]

        dates = self.start.strftime("%d/%m/%Y") + ' - ' + self.stop.strftime("%d/%m/%Y")
        excel = self.sage_excel(sorted(dic_info.items()), dates, company, self.stop)

        fp = BytesIO()
        excel.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        file_name = 'SAGE.xls'
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