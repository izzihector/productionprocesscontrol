# -*- coding: utf-8 -*-
from odoo import models, fields, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.addons.sale_subscription.models.sale_subscription import PERIODS
from odoo.tools import format_date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_type_id = fields.Many2one('sale.order.type', 'Type')

    sub_template_id = fields.Many2one('sale.subscription.template', 'Subscription template')

    sub_start = fields.Date()
    sub_end = fields.Date()

    def update_existing_subscriptions(self):
        """
        Heredamos para evitar que al hacer confirm a la orden
        desde el generar factura de la subscripcion, se tengan
        que actualizar los valores
        """
        res = []
        if self.env.context.get('from_subscription', False):
            return res
        else:
            return super(SaleOrder, self).update_existing_subscriptions()

    def _prepare_subscription_data(self, template):
        res = super(SaleOrder, self)._prepare_subscription_data(template)

        invoicing_period = relativedelta(**{PERIODS[template.recurring_rule_type]: template.recurring_interval})

        if template.recurring_rule_type == 'monthly':
            first_day = datetime.today().replace(day=1)
            recurring_next_date = first_day + invoicing_period
            res['recurring_next_date'] = recurring_next_date
        return res

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        subscription_id = self.mapped('order_line.subscription_id')
        if subscription_id:
            sub = subscription_id[0]

            lang = self.partner_invoice_id.lang
            if lang:
                self = self.with_context(lang=lang)

            invoicing_period = relativedelta(**{PERIODS[sub.recurring_rule_type]: sub.recurring_interval})
            recurring_next_invoice = fields.Date.from_string(sub.recurring_next_date)
            recurring_last_invoice = recurring_next_invoice - invoicing_period
            section_line = [(0, 0, {
                'name': _("Invoicing period: %s - %s") % (
                    format_date(self.env, recurring_last_invoice),
                    format_date(self.env, recurring_next_invoice - relativedelta(days=1))
                ),
                'display_type': 'line_section',
                'sequence': 0
            })]
            res['invoice_line_ids'] = section_line
        return res
