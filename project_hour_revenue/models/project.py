# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    alert_percentil_no_profitable = fields.Integer(
        string='Porcentaje de riesgo',
        required=False)

    type_project = fields.Selection(
        [('1', 'Mantenimiento'), ('2', 'Pack horas'), ('3', 'Proyecto cerrado'), ('4', 'Horas Facturables')],
        string='Tipo de proyecto',
        required=False
    )

    is_closed_project = fields.Boolean(
        string='Is closed Project',
        required=False)