# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "hr.department"

    project_id = fields.Many2one('project.project', string='Proyecto Preventa', domain="[('department_id', '=', id)]")