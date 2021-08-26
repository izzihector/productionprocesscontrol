# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'
    project_id_active = fields.Boolean(related='project_id.active')

    @api.model
    def create(self, vals):
        res = super(ProjectTask, self).create(vals)
        project_id = vals.get("project_id")
        if project_id:
            project = self.env['project.project'].browse(project_id)
            if not project.active:
                raise ValidationError(_("Can't task create to Archived project."))
        return res


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        res = super(AccountAnalyticLine, self).create(vals)
        project_id = vals.get("project_id")
        if project_id:
            project = self.env['project.project'].browse(project_id)
            if not project.active:
                raise ValidationError(_("Can't task create to Archived project."))
        return res
