# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    @api.depends('recurring_invoice_line_ids')
    def _compute_total_purchase_price(self):
        for subscription in self:
            subscription.total_purchase_price = sum(x.cost for x in self.recurring_invoice_line_ids)

    total_purchase_price = fields.Float(string='Total Purchase Price', compute='_compute_total_purchase_price',
                                        track_visibility='always')
    recurring_next_date = fields.Date(string='Date of Next Invoice', default=fields.Date.today, help="The next invoice will be created on this date then the period will be extended.",track_visibility='always')
