# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    total_horas_contratadas = fields.Integer(
        string='Total Horas Contratadas',
        required=False)

    total_horas_imputadas = fields.Integer(
        string='Total Horas Imputadas',
        required=False)

    horas_restantes_produccion = fields.Integer(
        string='Total Horas Restantes Produccion',
        required=False)

    alert_percentil_no_profitable = fields.Integer(
        string='Porcentaje de riesgo',
        required=False)

    type_project = fields.Selection(
        [('1', 'Mantenimiento'), ('2', 'Pack horas'), ('3', 'Proyecto cerrado')],
        string='Tipo de proyecto',
        required=True
    )

    #
    # BLOQUE 1
    # COMENTAMOS ESTE BLOQUE HASTA QUE ACTIVEMOS LAS HORAS QUE TIENE DISPONIBLES CADA TRABAJADOR EN EL PROYECTO
    # AHORA SE HACE SOBRE EL LISTADO KANBAN Y GENERA MUCHA CARGA EN LOS MISMOS
    #

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='kanban', toolbar=False, submenu=False):

    # PP = self.env['project.project']
    # PT = self.env['project.task']

    # projects = PP.search([])
    # for project in projects:
    #     total_quantity_for_project = 0
    #     total_worked_hours = 0
    #     horas_restantes_produccion = 0
    #     sales_lines = project.sale_line_id
    #     tasks = project.task_ids
    #
    #     if tasks:
    #         for task in tasks:
    #             sales_lines = task.sale_line_id
    #             total_worked_hours = total_worked_hours + task['effective_hours']
    #
    #             if sales_lines:
    #                 # obtenemos el total de cantidad por linea en el pedido
    #                 for sale_line in sales_lines:
    #                     total_quantity_line = sale_line['product_uom_qty']
    #                     total_quantity_for_project = total_quantity_for_project + total_quantity_line
    #
    #     project['total_horas_contratadas'] = total_quantity_for_project
    #
    #     horas_restantes_produccion = total_quantity_for_project - total_worked_hours
    #     project['total_horas_imputadas'] = total_worked_hours
    #     project['horas_restantes_produccion'] = horas_restantes_produccion
    #
    #     # if horas_restantes_produccion <= 0:
    #     #     project['hour_color_for_limit'] = "color:"
    # return super(Project, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                             submenu=submenu)

    # FIN BLOQUE 1
