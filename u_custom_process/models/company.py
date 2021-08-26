# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    project_allowed_ids = fields.Many2many(
        comodel_name='project.project',
        relation="res_company_project_allowed_rel"
    )