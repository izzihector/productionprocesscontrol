# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def compute_sales_hours(self):
        self.ensure_one()
        self.sales_hours = sum(self.task_ids.mapped('sales_hours'))

    sales_hours = fields.Float(
        'Sale hours',
        compute='compute_sales_hours'
    )

    department_id = fields.Many2one('hr.department', 'Department')

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def write(self, vals):
        for task in self:
            if vals.get('planned_hours', False) and not self.sales_hours:
                task.sales_hours = vals['planned_hours']
        return super(ProjectTask, self).write(vals)
    
    @api.model
    def create(self, vals_list):
        res = super(ProjectTask, self).create(vals_list)
        res.sales_hours = res.planned_hours
        return res

    @api.multi
    def unlink(self):
        for task in self:
            if task.sales_hours != 0:
                raise ValidationError(_("Task cannot be deleted!"))
        return super(ProjectTask, self).unlink()

    sales_hours = fields.Float(
        'Sale hours'
    )