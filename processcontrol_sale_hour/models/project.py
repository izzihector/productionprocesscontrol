# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Project(models.Model):
    _inherit = "project.project"
    _description = "Project"

    @api.multi
    def _compute_total_sale_hour(self):
        for project in self:
            total_sh = 0
            sol_obj = self.env['sale.order.line']
            project_sol = sol_obj.search([('project_id', '=', project.id)])
            for sol in project_sol:
                if sol.product_uom:
                    if 'hora' in sol.product_uom.name:
                        total_sh += float(sol.product_uom.name.rsplit(' hora')[0].replace(',', '.')) * sol.product_uom_qty
                    else:
                        total_sh += sol.product_uom_qty
            project.total_sale_hour = total_sh

    @api.multi
    def _compute_total_work_hour(self):
        for project in self:
            total_wh = 0
            aal_obj = self.env['account.analytic.line']
            project_aal = aal_obj.search([('project_id', '=', project.id)])
            for aal in project_aal:
                total_wh += aal.unit_amount
            project.total_work_hour = total_wh

    @api.depends('total_sale_hour', 'total_work_hour')
    def _compute_available_hour(self):
        for project in self:
            project.available_hour = project.total_sale_hour - project.total_work_hour

    total_sale_hour = fields.Float(string='Total Horas vendidas', compute='_compute_total_sale_hour')
    total_work_hour = fields.Float(string='Total horas trabajadas', compute='_compute_total_work_hour')
    available_hour = fields.Float(string='Total horas disponibles', compute='_compute_available_hour')
