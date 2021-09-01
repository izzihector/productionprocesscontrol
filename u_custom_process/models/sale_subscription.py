# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import format_date


_logger = logging.getLogger(__name__)

PERIODS = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}


#===============================================================================
# class SaleSubscriptionLine(models.Model):
#     _inherit = 'sale.subscription.line'
# 
#     @api.model
#     def create(self, vals_list):
#         sub_id = self.analytic_account_id
#         older_price = sum(x.cost for x in sub_id.recurring_invoice_line_ids)
#         res = super(SaleSubscriptionLine, self).create(vals_list)
# 
#         total_purchase_price = sum(x.cost for x in sub_id.recurring_invoice_line_ids)
#         content = ""
#         content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(
#             older_price) + "&#8594;" + "{:10.3f}".format(total_purchase_price) + "<br/>"
#         res.analytic_account_id.message_post(body=content)
#         return res
#===============================================================================


#===============================================================================
#     def unlink(self):
#         sub_id = self.analytic_account_id
#         older_price = sum(x.cost for x in sub_id.recurring_invoice_line_ids)
#         super(SaleSubscriptionLine, self).unlink()
# 
#         total_purchase_price = sum(x.cost for x in sub_id.recurring_invoice_line_ids)
#         content = ""
#         content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(
#             older_price) + "&#8594;" + "{:10.3f}".format(total_purchase_price) + "<br/>"
#         sub_id.message_post(body=content)
#===============================================================================


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"
    _description = "Subscription"

    @api.model
    def create(self, vals):
        """
        It is inherited to prepare the message in the creation of the order.

        @param vals:
        """
        res = super(SaleSubscription, self).create(vals)
        start_price = sum(x.cost for x in res.recurring_invoice_line_ids)
        content = "  \u2022 Precio Costo Total: " + "{:10.3f}".format(start_price) + "<br/>"
        res.message_post(body=content)

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


class SaleSubscriptionWizard(models.TransientModel):
    _inherit = 'sale.subscription.wizard'

    def create_sale_order(self):
        res = super(SaleSubscriptionWizard, self).create_sale_order()
        order_id = res.get('res_id', False)
        order = self.env['sale.order'].browse(order_id)
        subscription_id = self.env['sale.subscription'].browse(self.env.context.get('active_id', False))
        if subscription_id:
            order.sub_template_id = subscription_id.template_id.id
        return res
