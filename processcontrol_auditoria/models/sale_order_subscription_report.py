# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError
from xlwt import *
from io import BytesIO
import base64
from datetime import date
from dateutil.relativedelta import relativedelta


class sale_order_subscription_report(models.TransientModel):
    _name = 'sale.order.subscription.report'
    _description = 'Sale Order Subscription Report'

    def _get_default_start_date(self):
        today = date.today()
        return today.replace(day=1)

    def _get_default_stop_date(self):
        return date.today()

    name = fields.Char(string='Pedido de venta de subscripcion')
    start = fields.Date(string='Desde', required=True, default=_get_default_start_date)
    stop = fields.Date(string='Hasta', required=True, default=_get_default_stop_date)
    description = fields.Text(
        default='Reporte que puede devolver 3 hojas: Pedido de venta de subscripción, Pedido de venta con errores y Suscripciones sin ventas\n'
                '\n'
                'Pedido de venta de subscripción: esta hoja va a mostrar todos los pedidos de venta que la fecha de confrimación este\n'
                'dentro de los rangos de fechas ingresados y tenga una subscripción relacionada, si la base imponible del pedido\n'
                'de venta es diferente al precio recurrente de la subscripción esta se pinta de amarillo.\n'
                '\n'
                'Pedido de venta con errores: esta hoja va a mostrar todos los pedidos de venta que la fecha de confrimación este\n'
                'dentro de los rangos de fechas ingresados, sean de tipo subscripcion y no se encuentren una subscripción relacionada.\n'
                '\n'
                'Suscripciones sin ventas: esta hoja va a mostrar todas los suscripciones que deberian tener uno o varios pedido de venta creado\n'
                'dentro de los rangos de fechas ingresados y se encontraron menos, en el campo Detalle del error muestra cuantos\n'
                'pedidos de ventas deberian haber y cuantos se encontraron.\n',
        string='Descripción:', readonly=True)
    file = fields.Binary(string="Report")

    @staticmethod
    def get_next_interval(template, interval_date):
        if template.recurring_rule_type == 'daily':
            interval_date += relativedelta(days=template.recurring_interval)
        elif template.recurring_rule_type == 'weekly':
            interval_date += relativedelta(weeks=template.recurring_interval)
        elif template.recurring_rule_type == 'monthly':
            interval_date += relativedelta(months=template.recurring_interval)
        elif template.recurring_rule_type == 'yearly':
            interval_date += relativedelta(years=template.recurring_interval)
        else:
            raise UserError(_('Dont contemplate %s recurring interval type, communicate with TI') % template.recurring_rule_type)

        return interval_date

    def get_subscription_without_sales(self):
        subscription_without_sales = []
        in_process_stage_id = self.env['sale.subscription.stage'].search([('category', '=', 'progress')], limit=1).id
        subscriptions = self.env['sale.subscription'].search([('stage_id', '=', in_process_stage_id), ('date_start', '<=', self.stop), '|', ('date', '>=', self.start), ('date', '=', False)])
        for sub in subscriptions:
            so_count = 0
            interval_date = sub.date_start
            while interval_date <= self.stop:
                if interval_date >= self.start:
                    so_count += 1
                interval_date = self.get_next_interval(sub.template_id, interval_date)
            if so_count:
                so_list = []
                sol = self.env['sale.order.line']
                sol_ids = sol.search([('subscription_id', '=', sub.id)])
                for sol in sol_ids:
                    if sol.order_id.id not in so_list:
                        so_list.append(sol.order_id.id)
                if so_count > len(so_list):
                    subscription_without_sales.append([sub.name, sub.recurring_total, sub.template_id.name,
                                                       ('Should have %d but only found %d Sale Orders' % (so_count, len(so_list)))])

        return subscription_without_sales

    @staticmethod
    def sale_order_subscription_excel(sales_info_list, sales_error_list, subscription_without_sales):
        wb = Workbook(encoding='utf-8')
        row = 0
        title = easyxf('font: name Calibri, bold True; alignment: horizontal left')
        lines = easyxf('font: name Calibri; alignment: horizontal left')
        lines_number = easyxf('font: name Calibri; alignment: horizontal right',
                              num_format_str='#,##0.000;-#,##0.000;')
        lines_error = easyxf('font: name Calibri; alignment: horizontal left; pattern: pattern solid,'
                                      ' fore_colour light_yellow;')
        lines_number_error = easyxf('font: name Calibri; alignment: horizontal right; pattern: pattern solid,'
                                      ' fore_colour light_yellow;', num_format_str='#,##0.00;-#,##0.00;')
        lines_number_total = easyxf('font: name Calibri, bold True; alignment: horizontal right',
                              num_format_str='#,##0.000;-#,##0.000;')
        if sales_info_list:
            ws = wb.add_sheet('Pedido de venta de subscripción', cell_overwrite_ok=True)
            ws.write(row, 0, "Venta", title)
            ws.write(row, 1, "Cliente", title)
            ws.write(row, 2, "Subscripción", title)
            ws.write(row, 3, "Tipo de subscripción", title)
            ws.write(row, 4, "Fecha de confirmación", title)
            ws.write(row, 5, "Precio recurrente", title)
            ws.write(row, 6, "Total pedido de venta", title)
            for info in sales_info_list:
                row += 1
                if info[5] == info[6]:
                    ws.write(row, 0, info[0], lines)
                    ws.write(row, 1, info[1], lines)
                    ws.write(row, 2, info[2], lines)
                    ws.write(row, 3, info[3], lines)
                    ws.write(row, 4, info[4], lines)
                    ws.write(row, 5, info[5], lines_number)
                    ws.write(row, 6, info[6], lines_number)
                else:
                    ws.write(row, 0, info[0], lines_error)
                    ws.write(row, 1, info[1], lines_error)
                    ws.write(row, 2, info[2], lines_error)
                    ws.write(row, 3, info[3], lines_error)
                    ws.write(row, 4, info[4], lines_error)
                    ws.write(row, 5, info[5], lines_number_error)
                    ws.write(row, 6, info[6], lines_number_error)
            row += 1
            ws.write(row, 5, Formula("SUM(F1 :F%s)" % row), lines_number_total)
            ws.write(row, 6, Formula("SUM(G1 :G%s)" % row), lines_number_total)
            ws.col(0).width += 725
            ws.col(1).width += 725
            ws.col(2).width += 725
            ws.col(3).width += 725
            ws.col(4).width += 725
            ws.col(5).width += 725
            ws.col(6).width += 725

        if sales_error_list:
            row = 0
            ws = wb.add_sheet('Pedido de venta con errores', cell_overwrite_ok=True)
            ws.write(row, 0, "Venta", title)
            ws.write(row, 1, "Cliente", title)
            ws.write(row, 2, "Fecha de confirmación", title)
            ws.write(row, 3, "Total pedido de venta", title)
            for info_error in sales_error_list:
                row += 1
                ws.write(row, 0, info_error[0], lines)
                ws.write(row, 1, info_error[1], lines)
                ws.write(row, 2, info_error[2], lines)
                ws.write(row, 3, info_error[3], lines_number)
            ws.col(0).width += 725
            ws.col(1).width += 725
            ws.col(2).width += 725
            ws.col(3).width += 725

        if subscription_without_sales:
            row = 0
            ws = wb.add_sheet('Suscripciones sin ventas', cell_overwrite_ok=True)
            ws.write(row, 0, "Suscripción", title)
            ws.write(row, 1, "Precio Recurrente", title)
            ws.write(row, 2, "Tipo de Suscripción", title)
            ws.write(row, 3, "Detalle del error", title)
            for subs in subscription_without_sales:
                row += 1
                ws.write(row, 0, subs[0], lines)
                ws.write(row, 1, subs[1], lines_number)
                ws.write(row, 2, subs[2], lines)
                ws.write(row, 3, subs[3], lines)
            ws.col(0).width += 1500
            ws.col(1).width += 2000
            ws.col(2).width += 3000
            ws.col(3).width += 8000

        return wb

    def sale_order_subscription_report(self):
        subscription_type_id = self.env['sale.order.type'].search([('name', '=', u'Suscripción')], limit=1)
        if not subscription_type_id:
            raise UserError(_('Dont found the sale order type Subscription'))
        sale_order_with_subscription_ids = self.env['sale.order'].search([('sale_order_type_id', '=', subscription_type_id.id), ('date_order', '>=', self.start), ('date_order', '<=', self.stop), ('state', 'not in', ('draft', 'sent', 'cancel'))])
        if not sale_order_with_subscription_ids:
            raise UserError(_('Dont found any Sale Order from subscription in that range of dates'))
        sales_info_list = []
        sales_error_list = []
        for sale in sale_order_with_subscription_ids:
            info = []
            subscription = self.env['sale.subscription'].search([('code', '=', sale.origin)])
            if not sale.origin or not subscription:
                info.append(sale.name)
                info.append(sale.partner_id.name)
                info.append(sale.date_order.strftime("%d/%m/%Y"))
                info.append(sale.amount_untaxed)
                sales_error_list.append(info)
            else:
                if len(subscription) > 1:
                    raise UserError(_('Found more than one subscription with name %s' % sale.origin))
                info.append(sale.name)
                info.append(sale.partner_id.name)
                info.append(subscription.code)
                info.append(subscription.template_id.name)
                info.append(sale.date_order.strftime("%d/%m/%Y"))
                info.append(subscription.recurring_total)
                info.append(sale.amount_untaxed)
                sales_info_list.append(info)
        subscription_without_sales = self.get_subscription_without_sales()
        excel = self.sale_order_subscription_excel(sales_info_list, sales_error_list, subscription_without_sales)

        fp = BytesIO()
        excel.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        file_name = 'Pedido de venta de subscripcion.xls'
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