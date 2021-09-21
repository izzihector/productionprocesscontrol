# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class PlanningSlot(models.Model):
    _inherit = 'planning.slot'

    total_sale_hour = fields.Float(related='project_id.total_sale_hour',string='Horas vendidas',readonly=True)
    total_work_hour = fields.Float(related='project_id.total_work_hour',string='Horas trabajadas',readonly=True)
    available_hour = fields.Float(related='project_id.available_hour',string='Horas disponibles',readonly=True)
    partner_id = fields.Many2one(related='project_id.partner_id',string='Cliente',store=True)