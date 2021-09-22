# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.addons.sale_subscription.models.sale_subscription import PERIODS
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_date


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    payment_term_id = fields.Many2one('account.payment.term', 'Payment Terms')

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
        invoicing_period = relativedelta(**{PERIODS[self.recurring_rule_type]: self.recurring_interval})
        recurring_last_invoice = fields.Date.from_string(self.recurring_next_date)
        recurring_next_invoice = recurring_last_invoice + invoicing_period

        section_line = [(0, 0, {
            'name': _("Invoicing period: %s - %s") % (
                format_date(self.env, recurring_last_invoice),
                format_date(self.env, recurring_next_invoice - relativedelta(days=1))
            ),
            'display_type': 'line_section'
        })]
        return section_line + res

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

    def action_subscription_order(self):
        self.ensure_one()
        orders = self.env['sale.order'].search([('order_line.subscription_id', 'in', self.ids)])

        if len(orders) > 1:
            action = self.env["ir.actions.actions"]._for_xml_id("sale.action_orders")
            action['name'] = _('Quotations') if self.template_id.payment_mode == 'quotation_sale_order' else _(
                'Sales Orders')
            action['domain'] = [('id', 'in', orders.ids)]
            action['context'] = {"create": False}

        elif len(orders) == 1:
            action = {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'current',
                'res_model': 'sale.order',
                'res_id': orders.id
            }
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def generate_recurring_invoice(self):
        res = self._recurring_create_invoice()

        if res and res._table == 'sale_order':
            return self.action_subscription_order()
        elif res:
            return self.action_subscription_invoice()
        else:
            warning = """ Please check the selected subscription template:
    - Is there a fixed duration which is reached?
    - Do you configure your invoice method as "send & try to charge" or "Send after successful payment"?
            """
            raise UserError(warning)

    def _recurring_create_invoice(self, automatic=False):
        res = super(SaleSubscription, self)._recurring_create_invoice(automatic=automatic)

        current_date = date.today()
        domain = [
            ('recurring_next_date', '<=', current_date),
            '|', ('stage_category', '=', 'progress'),
            ('to_renew', '=', True)
        ]
        subscriptions = self.search(domain, limit=250)
        orders = self.env['sale.order']

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

                sub.with_context(skip_update_recurring_invoice_day=True).increment_period()
                orders += order_id

        if not res:
            return orders

        return res

    @api.model
    def create(self, vals):
        record = super(SaleSubscription, self).create(vals)
        self._create_line_subscription(record)
        return record

    def _create_line_subscription(self, record):
        recurring_invoice_line_ids = record.recurring_invoice_line_ids.filtered(
            lambda x: x.product_id.show_product)
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
