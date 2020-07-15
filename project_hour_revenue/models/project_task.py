# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError
import math


class ProjectTask(models.Model):
    _inherit = 'project.task'

    horas_restantes_produccion_proyecto = fields.Char(
        string='Total Horas Restantes Produccion',
        required=False, compute='_calc_hours_less_for_proyect')

    #     @api.multi
    #     def create(self, values):
    #         if values.get('project_id'):
    #         values['horas_restantes_produccion_proyecto'] = 800
    #         return super(ProjectTask, self).write(values)

    def _calc_hours_less_for_proyect(self):

        PP = self.env['project.project']
        PT = self.env['project.task']

        project_id = 0
        for task in self:
            project_id = task.project_id.id

        if project_id:

            projects = PP.search([('id', '=', project_id)])
            for project in projects:
                total_quantity_for_project = 0
                total_worked_hours = 0
                horas_restantes_produccion = 0
                sales_lines = project.sale_line_id
                tasks = project.task_ids

                if tasks:
                    for task in tasks:
                        sales_lines = task.sale_line_id
                        total_worked_hours = total_worked_hours + task['effective_hours']

                        if sales_lines:
                            # obtenemos el total de cantidad por linea en el pedido
                            for sale_line in sales_lines:
                                have_project = sale_line['x_studio_proyecto_pedido_venta']
                                total_quantity_line = sale_line['product_uom_qty']
                                horas_reales = sale_line['horas_reales']
                                if horas_reales:
                                    total_quantity_line = horas_reales
                                if have_project:
                                    total_quantity_line = sale_line['horas_reales']

                                total_quantity_for_project = total_quantity_for_project + total_quantity_line

                horas_restantes_produccion = total_quantity_for_project - total_worked_hours

                is_negative = 0
                negative_code = "-"

                if (negative_code in str(horas_restantes_produccion)):
                    is_negative = 1

                # if horas_restantes_produccion > 1:
                # horas = float(horas_restantes_produccion)

                seconds = abs(horas_restantes_produccion) * 60 * 60
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)

                horas_restantes_produccion = "%02d:%02d" % (hours, minutes)

                if is_negative == 1:
                    horas_restantes_produccion = "-" + horas_restantes_produccion

            self.horas_restantes_produccion_proyecto = horas_restantes_produccion

    def convert_time_unit_to_hours(self, time_unit):

        total_time_hour = 100
        total_minutes_hour = 60
        es_negativo = 0
        value_for_return = time_unit

        if time_unit < 0:
            es_negativo = 1
            time_unit = abs(time_unit)

        if es_negativo == 1:
            value_for_return = (time_unit * total_minutes_hour) / total_time_hour
            value_for_return = -abs(value_for_return)
        else:
            value_for_return = (time_unit * total_minutes_hour) / total_time_hour

        return value_for_return
