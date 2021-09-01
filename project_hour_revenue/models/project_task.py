# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError
import math


class ProjectTask(models.Model):
    _inherit = 'project.task'

    horas_restantes_produccion_proyecto = fields.Char(
        string='Total Horas Restantes Produccion',
        required=False)

