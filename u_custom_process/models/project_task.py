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
                raise ValidationError(_("No se puede crear/editar el registro ya que el proyecto se encuentra archivado"))
        return res

    def write(self, values):
        for record in self:
            if 'project_id' in values:
                project_id = values['project_id']
            else:
                project_id = record.project_id.id
            if 'active' not in values:
                if not record.active:
                    raise ValidationError(_("No se puede crear/editar el registro ya que la tarea se encuentra archivada"))

            project = self.env['project.project'].browse(project_id)
            if not project.active:
                raise ValidationError(_("No se puede crear/editar el registro ya que el proyecto se encuentra archivado"))
        return super(ProjectTask, self).write(values)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        res = super(AccountAnalyticLine, self).create(vals)
        project_id = vals.get("project_id")
        if project_id:
            project = self.env['project.project'].browse(project_id)
            if not project.active:
                raise ValidationError(_("No se puede crear/editar el registro ya que el proyecto se encuentra archivado"))
        return res

    def write(self, values):
        for record in self:
            if 'project_id' in values:
                project_id = values['project_id']
            else:
                project_id = record.project_id.id
            project = self.env['project.project'].browse(project_id)
            if not project.active:
                raise ValidationError(_("No se puede crear/editar el registro ya que el proyecto se encuentra archivado"))
        return super(AccountAnalyticLine, self).write(values)


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'


    def write(self, values):
        for record in self:
            if 'project_id' in values:
                project_id = values['project_id']
            else:
                project_id = record.project_id.id
            if 'active' not in values:
                if not record.active:
                    raise ValidationError(_("No se puede crear/editar el registro ya que el ticket se encuentra archivado"))

            project = self.env['project.project'].browse(project_id)
            if not project.active:
                raise ValidationError(_("No se puede crear/editar el registro ya que el proyecto se encuentra archivado"))
        return super(HelpdeskTicket, self).write(values)