# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import format_date


_logger = logging.getLogger(__name__)

PERIODS = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}


class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    @api.model
    def create(self, vals_list):
        sub_id = self.analytic_account_id
        older_price = sum(x.cost for x in sub_id.recurring_invoice_line_ids)
        res = super(SaleSubscriptionLine, self).create(vals_list)

        total_purchase_price = sum(x.cost for x in sub_id.recurring_invoice_line_ids)
        content = ""
        content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(
            older_price) + "&#8594;" + "{:10.3f}".format(total_purchase_price) + "<br/>"
        res.analytic_account_id.message_post(body=content)
        return res


    def unlink(self):
        sub_id = self.analytic_account_id
        older_price = sum(x.cost for x in sub_id.recurring_invoice_line_ids)
        super(SaleSubscriptionLine, self).unlink()

        total_purchase_price = sum(x.cost for x in sub_id.recurring_invoice_line_ids)
        content = ""
        content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(
            older_price) + "&#8594;" + "{:10.3f}".format(total_purchase_price) + "<br/>"
        sub_id.message_post(body=content)



class SaleSubscription(models.Model):
    _inherit = "sale.subscription"
    _description = "Subscription"

    def write(self, vals):
        older_price = sum(x.cost for x in self.recurring_invoice_line_ids)
        res = super(SaleSubscription, self).write(vals)
        if vals.get('recurring_invoice_line_ids'):
            for x in vals.get('recurring_invoice_line_ids'):
                if x[2] and x[2].get('cost'):
                    content = ""
                    total_purchase_price = sum(x.cost for x in self.recurring_invoice_line_ids)

                    content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(
                        older_price) + "&#8594;" + "{:10.3f}".format(total_purchase_price) + "<br/>"
                    self.message_post(body=content)
        return res
   
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
