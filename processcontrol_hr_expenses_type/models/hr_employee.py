# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    diet_limitless = fields.Boolean(string='Limitless Diet')
    discharge_date = fields.Date(string='Fecha de Alta')
    cod_employee = fields.Integer(string='Código')
