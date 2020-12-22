# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class SaleSubscriptionLine(models.Model):
    _name = "sale.subscription.line"
    _inherit = "sale.subscription.line"

    project_id = fields.Many2one('project.project', string='Project', required=False, auto_join=True)