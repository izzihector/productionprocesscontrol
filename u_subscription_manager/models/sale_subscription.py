# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
import logging
import datetime
import traceback
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    payment_term_id = fields.Many2one(
        'account.payment.term',
        'Payment Terms'
    )

    def _prepare_renewal_order_values(self):
        res = super(SaleSubscription, self)._prepare_renewal_order_values()
        for index, line in enumerate(res[self.id]['order_line']):
            line[2]['project_id'] = self.recurring_invoice_line_ids[index].project_id.id
            line[2]['cost'] = self.recurring_invoice_line_ids[index].cost
        res[self.id]['payment_term_id'] = self.payment_term_id.id
        res[self.id]['sale_order_type_id'] = self.template_id.sale_order_type_id.id
        return res

    @api.multi
    def _recurring_create_invoice(self, automatic=False):
        res = super(SaleSubscription, self)._recurring_create_invoice(automatic)
        current_date = datetime.date.today()
        domain = [('recurring_next_date', '<=', current_date),
                  '|', ('in_progress', '=', True),
                  ('to_renew', '=', True)]
        subscriptions = self.search(domain)
        for sub in subscriptions:
            if sub.template_id.payment_mode in ('quotation_sale_order', 'confirmed_sale_order'):
                values = sub._prepare_renewal_order_values()
                order_id = self.env['sale.order'].create(values[sub.id])
                order_id.subscription_id = sub.id
                order_id.order_line._compute_tax_id()

                if sub.template_id.payment_mode == 'confirmed_sale_order':
                    order_id.action_confirm()

                next_date = sub.recurring_next_date or current_date
                periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}

                invoicing_period = relativedelta(
                    **{periods[sub.recurring_rule_type]: sub.recurring_interval})
                new_date = next_date + invoicing_period

                sub.write({'recurring_next_date': new_date.strftime('%Y-%m-%d')})
        return res


class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    project_id = fields.Many2one(
        'project.project',
        'Project'
    )
    product_project_id = fields.Many2one(
        related='product_id.project_id'
    )
    cost = fields.Float(
        'Cost'
    )


class SaleSubscriptionTemplate(models.Model):
    _inherit = 'sale.subscription.template'

    payment_mode = fields.Selection(
        selection_add=[('quotation_sale_order', "Quotation"),
                       ('confirmed_sale_order', 'Confirmed Sale Order')]
    )
    sale_order_type_id = fields.Many2one(
        'sale.order.type',
        'Sale order type'
    )

