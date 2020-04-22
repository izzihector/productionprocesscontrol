# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
import base64
import csv
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class DataPbiExtractor(models.Model):
    _name = "data.pbi.extractor"

    name = fields.Char(string='Nombre')
    modelo = fields.Char(string='Modelo')

    file_name = fields.Char(string='File Name')
    file_binary = fields.Binary(string='Binary File')

    file_name_project_horas_vendidas_vs_realizadas = fields.Char(string='File Name Project Horas vs Vendidas')
    file_binary_project_horas_vendidas_vs_realizadas = fields.Binary(string='Binary File Project Horas vs Vendidas')

    @api.multi
    def get_informe_horas_vendidas_imputadas_analityc(self):
        now = datetime.now()  # current date and time

        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")

        filename = "analitica_proyectos_horas_vendidas_vs_imputadas_" + date_time + ".csv"

        with open("analitica_proyectos_horas_vendidas_vs_imputadas_" + date_time + ".csv", mode='w') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # create a row contains heading of each column
            # Proyecto y Tarea
            writer.writerow(
                ['Id proyecto', 'Proyecto', 'Cliente', 'Codigo Cliente', 'Tipo Proyecto', 'Responsable', 'Horas vendidas', 'Horas imputadas', '% Alerta'])

            PP = self.env['project.project']
            SSL = self.env['sale.subscription.line']
            AIL = self.env['account.invoice.line']

            projects = PP.search([])

            for project in projects:
                total_quantity_for_project = 0
                total_worked_hours = 0
                tasks = project.task_ids
                project_id = project.id
                project_name = project.name
                alert_percentil_no_profitable = 0
                nombre_cliente = project.partner_id.name
                codigo_cliente = project.partner_id.id
                tipo_proyecto = project.type_project
                responsable = project.user_id.name
                unidades_vendidas = 0

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

                total_horas_contratadas = total_quantity_for_project

                totalHorasContratadas = str(total_horas_contratadas)
                totalHorasContratadas = totalHorasContratadas.replace('.', ',')

                total_horas_imputadas = total_worked_hours

                totalHorasImputadas = str(total_horas_imputadas)
                totalHorasImputadas = totalHorasImputadas.replace('.', ',')


                if total_quantity_for_project == 0:
                    alert_percentil_no_profitable = 1000

                if total_worked_hours > 0 and total_quantity_for_project > 0:
                    # project['alert_percentil_no_profitable'] = (total_worked_hours * 100) / total_quantity_for_project
                    alert_percentil_no_profitable = (total_worked_hours * 100) / total_quantity_for_project

                writer.writerow([project_id, project_name, nombre_cliente, codigo_cliente, tipo_proyecto, responsable, totalHorasContratadas, totalHorasImputadas,
                                 alert_percentil_no_profitable])

        files = open(filename, 'rb').read()
        # file = open('export.csv', 'wb')
        #
        content = base64.encodestring(files)

        return self.write(
            {'file_name_project_horas_vendidas_vs_realizadas': filename,
             'file_binary_project_horas_vendidas_vs_realizadas': content, 'name': filename, 'model': 'PBI: Proyectos'})

    @api.multi
    def get_tickets_analityc(self):
        now = datetime.now()  # current date and time

        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")

        filename = "analitica_tickets_" + date_time + ".csv"

        with open("analitica_tickets_" + date_time + ".csv", mode='w') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # create a row contains heading of each column
            # Proyecto y Tarea
            writer.writerow(
                ['id', 'Nombre ticket', 'Empresa', 'Id Cliente', 'Descripción', 'Horas dedicadas', 'Equipo', 'Tarea',
                 'Proyecto', 'Fecha Creacion', 'Comercial'])

            HT = self.env['helpdesk.ticket']
            tickets = HT.search([])

            # fetch products and write respective data.
            for ticket in tickets:
                totalHorasImputadas = 0
                comercial = ticket.partner_id.user_id.name
                partes_horas = ticket.timesheet_ids
                tarea = ticket.task_id.name
                if tarea == False:
                    tarea = ""
                proyecto = ticket.project_id.name
                if partes_horas:
                    for account in partes_horas:
                        totalHorasImputadas = totalHorasImputadas + account.unit_amount
                name = ticket.name
                id = ticket.id
                partner = ticket.partner_name

                # Checkeamos si es compañia o no para ir a extraer el nombre correcto
                id_cliente = ticket.partner_id.id
                if ticket.partner_id.is_company == False:
                    partner = ticket.partner_id.parent_id.name
                    id_cliente = ticket.partner_id.parent_id.id

                descripcion = ticket.description
                if descripcion == False:
                    descripcion = ""
                fecha_creacion = ticket.create_date
                equipo = ticket.team_id
                totalHorasTexto = str(totalHorasImputadas)
                totalHorasTexto = totalHorasTexto.replace('.', ',')

                writer.writerow(
                    [id, name, partner, id_cliente, descripcion, totalHorasTexto, equipo.name, tarea, proyecto,
                     fecha_creacion.strftime("%d/%m/%Y"), comercial])

        files = open(filename, 'rb').read()
        # file = open('export.csv', 'wb')
        #
        content = base64.encodestring(files)

        return self.write(
            {'file_name': filename, 'file_binary': content, 'name': filename, 'model': 'PBI: Tickets'})
