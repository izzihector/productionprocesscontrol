# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import ValidationError

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

    file_name_tickets_sistemas = fields.Char(string='File Name Tickets Sistemas')
    file_binary_tickets_sistemas = fields.Binary(string='Binary File Tickets Sistemas')

    file_name_project_horas_vendidas_vs_realizadas = fields.Char(string='File Name Project Horas vs Vendidas')
    file_binary_project_horas_vendidas_vs_realizadas = fields.Binary(string='Binary File Project Horas vs Vendidas')

    @api.multi
    def get_informe_horas_vendidas_imputadas_analityc(self):
        # Controlar que es una devolucion: refund_invoice_id controla si tiene cantidades dvueltas (account.invoice)
        # Controlar que viene la fra de un pedido: origin (account.invoice)
        now = datetime.now()  # current date and time

        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")

        filename = "analitica_proyectos_horas_vendidas_vs_imputadas_" + date_time + ".csv"

        with open("analitica_proyectos_horas_vendidas_vs_imputadas_" + date_time + ".csv", mode='w') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # create a row contains heading of each column
            # Proyecto y Tarea
            writer.writerow(
                ['Id proyecto', 'Proyecto', 'Cliente', 'Codigo Cliente', 'Tipo Proyecto', 'Responsable',
                 'Horas vendidas', 'Horas presupuestadas', 'Horas Confirmadas', 'Horas totales', 'Horas imputadas', 'Proyecto Cerrado',
                 'Departamento', 'Comercial',
                 'Etapa'])

            PP = self.env['project.project']
            PT = self.env['project.task']
            SOL = self.env['sale.order.line']
            SSL = self.env['sale.subscription.line']
            AIL = self.env['account.invoice.line']

            projects = PP.search([])

            for project in projects:
                horas_proyecto_cerrado = 0
                is_closed_project = 0
                total_quantity_for_project = 0
                total_worked_hours = 0
                # tasks = project.task_ids
                project_id = project.id
                project_name = project.name
                alert_percentil_no_profitable = 0
                nombre_cliente = project.partner_id.name
                codigo_cliente = project.partner_id.id
                departamento = project.x_studio_departamento
                comercial = project.x_comercial_id.name
                tipo_proyecto = self._get_name_tipo_proyecto(project.type_project)
                responsable = project.user_id.name
                unidades_vendidas = 0
                proyectoCerrado = "NO"
                order_name = ""
                etapa = project.x_stage_id.display_name
                horas_confirmadas = 0
                horas_presupuestadas = 0
                horas_totales = 0

                # Primero visitamos las tareas para obtener las horas imputadas
                tasks = PT.search([('project_id', '=', project_id)])

                if tasks:
                    for task in tasks:
                        total_worked_hours = total_worked_hours + task['effective_hours']

                if project_id:
                    # Obtenemos las lineas de pedidos de venta que tienen asignado el proyecto
                    lineas_relacionadas_con_proyecto = SOL.search([
                        ('x_studio_proyecto_pedido_venta', '=', project_id)
                    ])

                    if lineas_relacionadas_con_proyecto:
                        # obtenemos el total de cantidad por linea en el pedido
                        for sale_line in lineas_relacionadas_con_proyecto:
                            total_quantity_line = sale_line['product_uom_qty']

                            # Comprobamos si el pedido de esta linea tiene factura, si la tiene
                            # comprobamos que no tiene refounds, si los tiene, no sumamos la cantidad de horas
                            # vendidas
                            # COGEMOS EL PEDIDO EN ORDER_NAME
                            order_name = sale_line['order_id'].name
                            order_state = sale_line['order_id'].state

                            # Comprobamos si tiene factura
                            #if self.tiene_factura(order_name) == 1:
                            if sale_line['order_id'].invoice_status == 'invoiced' or sale_line['order_id'].invoice_status == 'upselling':

                                # Comprobamos que la factura no es devolucion y el pedido no esta cancelado
                                # posteriormente, añadimos las horas al total para contabilizarlas contra las imputadas
                                if self.descartar_facturas_devolucion(
                                        order_name) == 0 and self.check_order_is_active(order_state) == 1:
                                    total_quantity_for_project = total_quantity_for_project + total_quantity_line
                                    if sale_line.horas_reales > 0:
                                        is_closed_project = 1
                                        proyectoCerrado = "SI"
                                        horas_proyecto_cerrado = horas_proyecto_cerrado + sale_line.horas_reales
                            else:
                                # Obtenemos los sumatorios de horas presupuestasas y horas confirmadas
                                if order_state == "draft":
                                    if sale_line.horas_reales > 0:
                                        is_closed_project = 1
                                        proyectoCerrado = "SI"
                                        horas_proyecto_cerrado = horas_proyecto_cerrado + sale_line.horas_reales
                                        horas_presupuestadas = horas_presupuestadas + sale_line.horas_reales
                                    else:
                                        horas_presupuestadas = horas_presupuestadas + total_quantity_line
                                elif order_state == "sent":
                                    if sale_line.horas_reales > 0:
                                        is_closed_project = 1
                                        proyectoCerrado = "SI"
                                        horas_proyecto_cerrado = horas_proyecto_cerrado + sale_line.horas_reales
                                        horas_presupuestadas = horas_presupuestadas + sale_line.horas_reales
                                    else:
                                        horas_presupuestadas = horas_presupuestadas + total_quantity_line
                                elif order_state == "sale":
                                    if sale_line.horas_reales > 0:
                                        is_closed_project = 1
                                        proyectoCerrado = "SI"
                                        horas_proyecto_cerrado = horas_proyecto_cerrado + sale_line.horas_reales
                                        horas_confirmadas = horas_confirmadas + sale_line.horas_reales
                                    else:
                                        horas_confirmadas = horas_confirmadas + total_quantity_line

                    subscription_lines = SSL.search([
                        ('project_id', '=', project_id)
                    ])
                    if subscription_lines:
                        for suscription_line in subscription_lines:
                            subscription_id = suscription_line.analytic_account_id
                            # Obtenemos las facturas de su suscripcion para recorrer las lineas de las mismas
                            if subscription_id:
                                for sub in subscription_id:
                                    invoice_lines = AIL.search([
                                        ('subscription_id', '=', sub.id)
                                    ])

                                    if invoice_lines:
                                        for invoice_line in invoice_lines:
                                            if invoice_line.project_id.id == project_id:
                                                total_quantity_for_project = total_quantity_for_project + invoice_line[
                                                    'quantity']

                total_horas_contratadas = total_quantity_for_project
                horas_totales = horas_confirmadas + total_horas_contratadas

                if is_closed_project == 1:
                    total_horas_contratadas = horas_proyecto_cerrado

                totalHorasContratadas = str(total_horas_contratadas)
                totalHorasContratadas = totalHorasContratadas.replace('.', ',')

                total_horas_imputadas = total_worked_hours
                # totalHorasImputadas = total_worked_hours

                totalHorasImputadas = str(total_horas_imputadas)
                totalHorasImputadas = totalHorasImputadas.replace('.', ',')

                if total_quantity_for_project == 0:
                    alert_percentil_no_profitable = 1000

                if total_worked_hours > 0 and total_quantity_for_project > 0:
                    # project['alert_percentil_no_profitable'] = (total_worked_hours * 100) / total_quantity_for_project
                    alert_percentil_no_profitable = (total_worked_hours * 100) / total_quantity_for_project


                writer.writerow([project_id, project_name, nombre_cliente, codigo_cliente, tipo_proyecto, responsable,
                                 totalHorasContratadas, horas_presupuestadas, horas_confirmadas, horas_totales,
                                 totalHorasImputadas, proyectoCerrado, departamento, comercial, etapa])

        files = open(filename, 'rb').read()
        # file = open('export.csv', 'wb')
        #
        content = base64.encodestring(files)

        return self.write(
            {'file_name_project_horas_vendidas_vs_realizadas': filename,
             'file_binary_project_horas_vendidas_vs_realizadas': content, 'name': filename, 'model': 'PBI: Proyectos'})

    def check_order_is_active(self, estado_pedido):
        if estado_pedido == "cancel":
            return 0

        return 1

    def descartar_facturas_devolucion(self, nombre_pedido_venta):
        AI = self.env['account.invoice']
        #Este tambien hay que cambiarlo por un IN o derivado
        facturas = AI.search([('origin', '=', nombre_pedido_venta)])

        if facturas:
            for factura in facturas:
                facturas_devueltas = factura['refund_invoice_ids']
                if facturas_devueltas:
                    # Tiene devolucion, no lo contabilizamos
                    return 1
                else:
                    return 0

        return 0

    def tiene_factura(self, nombre_pedido_venta):
        AI = self.env['account.invoice']
        facturas = AI.search([])
        if facturas:
            for factura in facturas:
                origenes = factura['origin']
                origenes_array = origenes.split(',')
                if origenes_array:
                    for origen in origenes_array:
                        if origen == nombre_pedido_venta:
                            return 1
        return 0

    def _get_name_tipo_proyecto(self, idproyecto):
        resultado = "Sin definir"
        if idproyecto == "1":
            resultado = "Mantenimiento"
        if idproyecto == "2":
            resultado = "Pack horas"
        if idproyecto == "3":
            resultado = "Proyecto cerrado"
        if idproyecto == "4":
            resultado = "Horas facturables"

        return resultado

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

    @api.multi
    def get_tickets_sistemas_analityc(self):
        now = datetime.now()  # current date and time

        date_time = now.strftime("%m_%d_%Y_%H_%M_%S")

        filename = "analitica_tickets_sistemas_" + date_time + ".csv"

        with open("analitica_tickets_sistemas_" + date_time + ".csv", mode='w') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # create a row contains heading of each column
            # Proyecto y Tarea
            writer.writerow(
                ['id', 'Nombre ticket', 'Empresa', 'Id Cliente', 'Descripción', 'Horas dedicadas', 'Equipo', 'Tarea',
                 'Proyecto', 'Fecha Creacion', 'Comercial', 'Hora Creacion', 'Dia de la semana', 'Tecnico'])

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
                tecnico = ticket.user_id.name

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

                # Seteamos el lenguaje de fechas a español
                locale.setlocale(locale.LC_ALL, "es_ES.utf8")

                writer.writerow(
                    [id, name, partner, id_cliente, descripcion, totalHorasTexto, equipo.name, tarea, proyecto,
                     fecha_creacion.strftime("%d/%m/%Y"), comercial, fecha_creacion.strftime("%H:%M:%S"),
                     fecha_creacion.strftime("%A"), tecnico])

        files = open(filename, 'rb').read()
        # file = open('export.csv', 'wb')
        #
        content = base64.encodestring(files)

        return self.write(
            {'file_name_tickets_sistemas': filename, 'file_binary_tickets_sistemas': content, 'name': filename,
             'model': 'PBI: Tickets Sistemas'})
