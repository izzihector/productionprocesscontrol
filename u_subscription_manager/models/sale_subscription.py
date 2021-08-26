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

    def _prepare_renewal_order_values(self, discard_product_ids=False, new_lines_ids=False):
        res = super(SaleSubscription, self)._prepare_renewal_order_values()
        for index, line in enumerate(res[self.id]['order_line']):
            line[2]['project_id'] = self.recurring_invoice_line_ids[index].project_id.id
            line[2]['purchase_price'] = self.recurring_invoice_line_ids[index].cost
            line[2]['name'] = self.recurring_invoice_line_ids[index].name
            line[2]['display_type'] = self.recurring_invoice_line_ids[index].display_type
        res[self.id]['payment_term_id'] = self.payment_term_id.id
        res[self.id]['sale_order_type_id'] = self.template_id.sale_order_type_id.id
        return res

    #@api.multi
    def _recurring_create_invoice(self, automatic=False):
        res = super(SaleSubscription, self)._recurring_create_invoice(automatic=automatic)
        current_date = date.today()
        domain = [('recurring_next_date', '<=', current_date),
                  '|', ('stage_category', '=', 'progress'),
                  ('to_renew', '=', True)]
        subscriptions = self.search(domain, limit=250)
        for sub in subscriptions:
            if sub.template_id.payment_mode in ('quotation_sale_order', 'confirmed_sale_order'):
                values = sub._prepare_renewal_order_values()
                order_id = self.env['sale.order'].create(values[sub.id])
                order_id.description = sub.display_name
                order_id.order_line.subscription_id = sub.id
                order_id.order_line._compute_tax_id()
                order_id.sub_template_id = sub.template_id.id

                if sub.template_id.payment_mode == 'confirmed_sale_order':
                    order_id.with_context(from_subscription=True).action_confirm()

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
        self._create_line_subscription(record)
        return record

    def _create_line_subscription(self, record):
        recurring_invoice_line_ids = record.recurring_invoice_line_ids.filtered(lambda x: x.product_id.show_product == True)
        list_task = self.env['project.task'].search([('partner_id', '=', record.partner_id.id)])

        line_vals = []
        for line in recurring_invoice_line_ids:
            params = {
                'product_id': line.product_id.id,
                'sale_subscription_line_id': line.id,
            }
            line_vals.append((0, 0, params))
        list_task.update({
            'product_subscription': line_vals
        })
        return

class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'
    _order = 'sequence'

    sequence = fields.Integer(
        string='Sequence',
        default=1
    )
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
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")],
        default=False,
        help="Technical field for UX purpose."
    )
    product_id = fields.Many2one(
        required=False
    )
    uom_id = fields.Many2one(
        required=False
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_type', self.default_get(['display_type'])['display_type']):
                vals.update(product_id=False, price_unit=0, product_uom_qty=0,
                            product_uom=False)
        return super(SaleSubscriptionLine, self).create(vals_list)

    #@api.multi
    def write(self, values):
        if 'display_type' in values and self.filtered(
                lambda line: line.display_type != values.get('display_type')):
            raise UserError(_(
                "You cannot change the type of an sale order line. Instead you "
                "should delete the current line and create a new line of "
                "the proper type."))
        return super(SaleSubscriptionLine, self).write(values)


class SaleSubscriptionTemplate(models.Model):
    _inherit = 'sale.subscription.template'

    payment_mode = fields.Selection(
        selection_add=[('quotation_sale_order', "Quotation"),
                       ('confirmed_sale_order', 'Confirmed Sale Order')], ondelete={'quotation_sale_order': 'set default', 'confirmed_sale_order': 'set default'}
    )
    sale_order_type_id = fields.Many2one(
        'sale.order.type',
        'Sale order type'
    )

