# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
import logging
from datetime import datetime, date
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
    product_ticket_task_line = fields.One2many('product.ticket.task', 'sale_subscription_id', string='Task and ticket product line')
    ticket_task_total = fields.Float(compute='_compute_ticket_task_total', string="Total", store=True)

    def _prepare_renewal_order_values(self):
        res = super(SaleSubscription, self)._prepare_renewal_order_values()
        for index, line in enumerate(res[self.id]['order_line']):
            line[2]['project_id'] = self.recurring_invoice_line_ids[index].project_id.id
            line[2]['purchase_price'] = self.recurring_invoice_line_ids[index].cost
            line[2]['name'] = self.recurring_invoice_line_ids[index].name
        res[self.id]['payment_term_id'] = self.payment_term_id.id
        res[self.id]['sale_order_type_id'] = self.template_id.sale_order_type_id.id
        return res

    @api.multi
    def _recurring_create_invoice(self, automatic=False):
        res = super(SaleSubscription, self)._recurring_create_invoice(automatic)
        current_date = date.today()
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

                if sub.template_id.recurring_rule_type == 'monthly':
                    first_day = datetime.today().replace(day=1)
                    recurring_next_date = first_day + invoicing_period
                    new_date = recurring_next_date
                else:
                    new_date = next_date + invoicing_period

                sub.write({'recurring_next_date': new_date.strftime('%Y-%m-%d')})
        return res

    @api.model
    def create(self, vals):
        record = super(SaleSubscription, self).create(vals)
        recurring_invoice_line_ids = record.recurring_invoice_line_ids.filtered(lambda x: x.product_id.type == 'service' and
                                                x.product_id.recurring_invoice == True and x.product_id.show_product == True)

        line_vals = []
        for line in recurring_invoice_line_ids:
            params = {
                'product_id': line.product_id.id,
                'sale_subscription_line_id': line.id,
            }
            line_vals.append((0, 0, params))
        record.update({
            'product_ticket_task_line': line_vals
        })
        return record

    @api.multi
    def write(self, vals):
        record= super(SaleSubscription, self).write(vals)

        if vals.get('recurring_invoice_line_ids'):
            product_list= [x[2]['product_id'] for x in vals['recurring_invoice_line_ids'] if x[2] != False]
            lines= self.recurring_invoice_line_ids.filtered(lambda x: x.product_id.id in product_list and x.product_id.type == 'service' and
                                                    x.product_id.recurring_invoice == True and x.product_id.show_product == True)

            line_vals = []
            for line in lines:
                params = {
                    'product_id': line.product_id.id,
                    'sale_subscription_line_id': line.id,
                }
                line_vals.append((0, 0, params))
            self.update({
                'product_ticket_task_line': line_vals
            })
        return record

    @api.depends('product_ticket_task_line', 'product_ticket_task_line.quantity', 'product_ticket_task_line.price_subtotal')
    def _compute_ticket_task_total(self):
        for aux in self:
            aux.ticket_task_total = sum(line.price_subtotal for line in aux.product_ticket_task_line)

class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    product_service_tracking = fields.Selection(
        related='product_id.service_tracking'
    )
    cost = fields.Float(
        'Cost'
    )
    order_line_id = fields.Many2one(
        'sale.order.line',
        'Order line'
    )
    project_id = fields.Many2one(
        'project.project',
        'Project'
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

