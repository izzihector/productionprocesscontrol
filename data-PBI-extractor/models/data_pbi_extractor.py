# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
import base64
import csv
from datetime import datetime


class DataPbiExtractor(models.Model):
    _name = "data.pbi.extractor"

    name = fields.Char(string='Nombre')
    modelo = fields.Char(string='Modelo')
    file_name = fields.Char(string='File Name')
    file_binary = fields.Binary(string='Binary File')

    @api.multi
    def get_tickets_analityc(self):
        now = datetime.now()  # current date and time

        date_time = now.strftime("%m_%d_%Y")

        filename = "analitica_tickets_" + date_time + ".csv"

        with open("analitica_tickets_" + date_time + ".csv", mode='w') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # create a row contains heading of each column
            # Proyecto y Tarea
            writer.writerow(
                ['id', 'Nombre ticket', 'Empresa', 'Id Cliente', 'Descripción', 'Horas dedicadas', 'Equipo', 'Tarea', 'Proyecto', 'Fecha Creacion'])

            HT = self.env['helpdesk.ticket']
            tickets = HT.search([])

            # fetch products and write respective data.
            for ticket in tickets:
                totalHorasImputadas = 0
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
                if ticket.partner_id.is_company == False:
                    partner = ticket.partner_id.parent_id.name
                    id_cliente = ticket.partner_id.parent_id.id

                descripcion = ticket.description
                if descripcion == False:
                    descripcion = ""
                fecha_creacion = ticket.create_date
                equipo = ticket.team_id
                writer.writerow([id, name, partner, id_cliente, descripcion, totalHorasImputadas, equipo.name, tarea, proyecto,
                                 fecha_creacion.strftime("%m/%d/%Y")])

        files = open(filename, 'rb').read()
        # file = open('export.csv', 'wb')
        #
        content = base64.encodestring(files)

        return self.write(
            {'file_name': filename, 'file_binary': content, 'name': filename, 'model': 'PBI: Tickets'})
