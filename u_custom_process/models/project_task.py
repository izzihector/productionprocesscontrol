# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError
import math


class ProjectTask(models.Model):
    _inherit = 'project.task'

    opportunity_id = fields.Many2one('crm.lead')
    process_type = fields.Selection(
        [('normal', 'Normal'),('tech', 'Technical')],
        default='normal'
    )

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
