# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

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

