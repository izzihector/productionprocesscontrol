# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    total_purchase_price = fields.Float(string='Total Purchase Price', compute='_compute_total_purchase_price',
                                        tracking=True, store=True)
    recurring_next_date = fields.Date(
        string='Date of Next Invoice', default=fields.Date.today,
        help="The next invoice will be created on this date then the period will be extended.",
        tracking=True
    )

    @api.depends('recurring_invoice_line_ids')
    def _compute_total_purchase_price(self):
        for subscription in self:
            subscription.total_purchase_price = sum(subscription.recurring_invoice_line_ids.mapped('cost'))
