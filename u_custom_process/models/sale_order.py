# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    

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
