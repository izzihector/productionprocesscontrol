# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools import format_date, float_compare
from dateutil.relativedelta import relativedelta

PERIODS = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sub_template_id = fields.Many2one(
        'sale.subscription.template',
        'Subscription template'
    )

    @api.model
    def create(self, vals):
        """
        It is inherited to prepare the message in the creation of the order.
        
        @param vals:
        """
        res = super(SaleOrder, self).create(vals)
        older_price = sum(x.purchase_price for x in res.order_line)
        content = ""
        content = content + "  \u2022 Precio Costo Total: " + "{:10.3f}".format(older_price) + "<br/>"
        content = content + "  \u2022 Margen: " + "{:10.3f}".format(res.margin) + "<br/>"
        res.message_post(body=content)
 
        return res

    def prepare_message_post(self,older_price,margin):      
        """
        A function that prepares the message in the order.
        
        @param older_price:
        @param margin:
        """
        
        content = ""
        total_purchase_price = sum(x.purchase_price for x in self.order_line)
        content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(older_price) + "&#8594;" + "{:10.3f}".format(total_purchase_price) + "<br/>"
        content = content + "  \u2022 Margen: " + "{:10.3f}".format(margin) + "&#8594;" + "{:10.3f}".format(self.margin) + "<br/>"
        
        return content
    
    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        subscription_id = self.mapped('order_line.subscription_id')
        if subscription_id:
            subscription_id = subscription_id[0]
            date_start = subscription_id.recurring_next_date
            date_stop = date_start + relativedelta(
                **{PERIODS[subscription_id.recurring_rule_type]: subscription_id.recurring_interval}) \
                        - relativedelta(
                days=1)

            lang = self.partner_invoice_id.lang
            format_date = self.env['ir.qweb.field.date'].with_context(lang=lang).value_to_html
            # Ugly workaround to display the description in the correct language
            if lang:
                self = self.with_context(lang=lang)

            period_msg = _("Invoicing period: %s - %s") % (
            format_date(fields.Date.to_string(date_start), {}),
            format_date(fields.Date.to_string(date_stop), {}))
            section_line = [(0, 0, {
                'name': period_msg,
                'display_type': 'line_section',
                'sequence': 0
            })]
            res['invoice_line_ids'] = section_line
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

#===============================================================================
#     def unlink(self):
#         import pdb;pdb.set_trace()
#         older_price = sum(x.purchase_price for x in self)
#         margin = self.order_id.margin
#         total_purchase_price = sum(x.purchase_price for x in self)
#  
#          
#          
# #         for x in self:
# #             if  x.get('purchase_price'):
#         content = ""
#         content = content + "  \u2022 Precio Costo: " + "{:10.3f}".format(
#             older_price) + "&#8594;" + "{:10.3f}".format(total_purchase_price) + "<br/>"
#         content = content + "  \u2022 Margen: " + "{:10.3f}".format(margin) \
#                   + "&#8594;" + "{:10.3f}".format(
#             self.order_id.margin) + "<br/>"
#         self.order_id.message_post(body=content)
#         res = super(SaleOrderLine, self).unlink()
#         return res
#===============================================================================

  #=============================================================================
  #   @api.model
  #   def create(self, vals):
  #       res = super(SaleOrderLine, self).create(vals)
  #       if vals.get("purchase_price"):
  #           content = ""
  #           content = content + "  \u2022 Precio Costo: " + "{:10.3f}"\
  #               .format(vals.get("purchase_price")) + "<br/>"
  #           res.order_id.message_post(body=content)
  # 
  #       return res
  #=============================================================================

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
