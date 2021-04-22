# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    project_allowed_ids = fields.Many2many(
        comodel_name='project.project',
        readonly=False,
        related='company_id.project_allowed_ids'
    )
