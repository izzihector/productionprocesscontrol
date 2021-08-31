# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ProjectHourRevenueReportWizard(models.TransientModel):
    _name = 'project.hour.revenue.report.wizard'

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    id_responsable = fields.Many2one('res.users', string='Worker')
    departamento = fields.Selection(
        [('Sistemas', 'Sistemas'), ('Software', 'Software')],
        string='Departamento')

    #@api.multi
    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start, 'date_end': self.date_end, 'id_responsable': self.id_responsable.id,
                'departamento': self.departamento,
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('project_hour_revenue.project_hour_revenue_summary').report_action(
            self, data=data)


class ProjectHourRevenueReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.project_hour_revenue.revenue_summary_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        id_responsable = data['form']['id_responsable']
        departamento = data['form']['departamento']

        PP = self.env['project.project']
        PT = self.env['project.task']
        SOL = self.env['sale.order.line']
        SSL = self.env['sale.subscription.line']
        AIL = self.env['account.invoice.line']

        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        delta = timedelta(days=1)

        docs = []

        while start_date <= end_date:
            date = start_date
            start_date += delta
            projects = PP.search([
                ('create_date', '>=', date.strftime(DATETIME_FORMAT)),
                ('create_date', '<', start_date.strftime(DATETIME_FORMAT))
            ])

            if id_responsable > 0 and departamento is not False:
                projects = PP.search([
                    ('create_date', '>=', date.strftime(DATETIME_FORMAT)),
                    ('create_date', '<', start_date.strftime(DATETIME_FORMAT)),
                    ('user_id', '=', id_responsable),
                    ('x_studio_departamento', '=', departamento)
                ])

            if id_responsable > 0 and departamento is False:
                projects = PP.search([
                    ('create_date', '>=', date.strftime(DATETIME_FORMAT)),
                    ('create_date', '<', start_date.strftime(DATETIME_FORMAT)),
                    ('user_id', '=', id_responsable)
                ])

            if departamento is not False and id_responsable == 0:
                projects = PP.search([
                    ('create_date', '>=', date.strftime(DATETIME_FORMAT)),
                    ('create_date', '<', start_date.strftime(DATETIME_FORMAT)),
                    ('x_studio_departamento', '=', departamento)
                ])
            #
            # if departamento and user_id == "":
            #     projects = PP.search([
            #         ('create_date', '>=', date.strftime(DATETIME_FORMAT)),
            #         ('create_date', '<', start_date.strftime(DATETIME_FORMAT)),
            #         ('x_studio_departamento', '=', departamento)
            #     ])

            for project in projects:
                # project['is_closed_project'] = False
                horas_proyecto_cerrado = 0
                is_closed_project = 0
                total_quantity_for_project = 0
                total_worked_hours = 0
                tasks = project.task_ids
                project_id = project.id

                # Primero visitamos las tareas para obtener las horas imputadas y si estas tareas
                # tienen lineas de venta, las recogemos con el fin de ir acumulando
                # las horas vendidas
                if tasks:
                    for task in tasks:
                        sales_lines = task.sale_line_id
                        total_worked_hours = total_worked_hours + task['effective_hours']

                        if sales_lines:
                            # obtenemos el total de cantidad por linea en el pedido
                            for sale_line in sales_lines:
                                if sale_line.horas_reales > 0:
                                    is_closed_project = 1
                                    # project['is_closed_project'] = True
                                    horas_proyecto_cerrado = horas_proyecto_cerrado + sale_line.horas_reales
                                total_quantity_line = sale_line['product_uom_qty']
                                total_quantity_for_project = total_quantity_for_project + total_quantity_line

                if project_id:
                    subscription_lines = SSL.search([
                        ('project_id', '=', project_id)
                    ])
                    if subscription_lines:
                        subscription_id = subscription_lines.analytic_account_id.id
                        # Obtenemos las facturas de su suscripcion para recorrer las lineas de las mismas
                        if subscription_id:
                            invoice_lines = AIL.search([
                                ('subscription_id', '=', subscription_id)
                            ])
                            if invoice_lines:
                                for invoice_line in invoice_lines:
                                    total_quantity_for_project = total_quantity_for_project + invoice_line['quantity']

                project['total_horas_contratadas'] = total_quantity_for_project

                if is_closed_project == 1:
                    project['total_horas_contratadas'] = horas_proyecto_cerrado

                project['total_horas_imputadas'] = total_worked_hours

                if total_quantity_for_project == 0:
                    project['alert_percentil_no_profitable'] = 1000

                if total_worked_hours > 0 and total_quantity_for_project > 0:
                    # project['alert_percentil_no_profitable'] = (total_worked_hours * 100) / total_quantity_for_project
                    project['alert_percentil_no_profitable'] = (total_worked_hours * 100) / total_quantity_for_project

            docs.append({
                'date': date.strftime("%Y-%m-%d"),
                'company': self.env.user.company_id,
                'projects': projects
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }
