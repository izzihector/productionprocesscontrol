# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    horas_restantes_produccion_proyecto = fields.Integer(
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
                                total_quantity_line = sale_line['product_uom_qty']
                                total_quantity_for_project = total_quantity_for_project + total_quantity_line

                        horas_restantes_produccion = total_quantity_for_project - total_worked_hours

                        task['horas_restantes_produccion_proyecto'] = horas_restantes_produccion

                # Queda comentado ya que no atacamos al proyecto
                # project['total_horas_contratadas'] = total_quantity_for_project
                # project['total_horas_imputadas'] = total_worked_hours
                # project['horas_restantes_produccion'] = horas_restantes_produccion

                # Asignamos a la tarea

        return res

#                 if horas_restantes_produccion <= 0:
#                     project['hour_color_for_limit'] = "color:"
#         return super(ProjectTask, self).fields_view_get(view_id=None, view_type='form', toolbar=False, submenu=False)

