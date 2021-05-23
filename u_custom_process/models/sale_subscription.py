# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import format_date


_logger = logging.getLogger(__name__)

PERIODS = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"
    _description = "Subscription"
   
    def _prepare_invoice_lines(self, fiscal_position):
        res = super()._prepare_invoice_lines(fiscal_position)
        date_start = self.recurring_next_date
        date_stop = date_start + relativedelta(**{PERIODS[self.recurring_rule_type]:
                                                      self.recurring_interval}) - relativedelta(days=1)
        period_msg = _("Invoicing period: %s - %s") % (format_date(fields.Date.to_string(date_start), {}),
                                                       format_date(fields.Date.to_string(date_stop), {}))
        section_line = [(0, 0, {
            'name':  period_msg,
            'display_type': 'line_section'
        })]
        return section_line + res
