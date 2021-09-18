# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    cliente_id = fields.Many2one(related='helpdesk_ticket_id.partner_id.parent_id',string='Cliente del ticket',store=True)
