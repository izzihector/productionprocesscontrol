# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools import format_date, float_compare
from dateutil.relativedelta import relativedelta

PERIODS = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        subscription_id = self.mapped('order_line.subscription_id')[0]
        date_start = subscription_id.recurring_next_date
        date_stop = date_start + relativedelta(**{PERIODS[subscription_id.recurring_rule_type]: subscription_id.recurring_interval}) - relativedelta(days=1)

        lang = self.partner_invoice_id.lang
        format_date = self.env['ir.qweb.field.date'].with_context(lang=lang).value_to_html
        # Ugly workaround to display the description in the correct language
        if lang:
            self = self.with_context(lang=lang)

        period_msg = _("Invoicing period: %s - %s") % (format_date(fields.Date.to_string(date_start), {}), format_date(fields.Date.to_string(date_stop), {}))
        section_line = [(0, 0, {
            'name':  period_msg,
            'display_type': 'line_section',
            'sequence': 0
        })]
        res['invoice_line_ids'] = section_line
        return res

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        if vals.get("purchase_price"):
            content = ""
            content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(vals.get("purchase_price")) + "<br/>"
            res.order_id.message_post(body=content)

        return res

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        content = ""
        if vals.get("purchase_price"):
            content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(vals.get("purchase_price")) + "<br/>"
            self.order_id.message_post(body=content)

        return res  

    def _prepare_invoice_line(self, **optional_values):
        """
        Override to add subscription-specific behaviours.

        Display the invoicing period in the invoice line description, link the invoice line to the
        correct subscription and to the subscription's analytic account if present, add revenue dates.
        """
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)  # <-- ensure_one()
        if self.subscription_id:
            res.update({
                'name': self.name
            })            
        return res
