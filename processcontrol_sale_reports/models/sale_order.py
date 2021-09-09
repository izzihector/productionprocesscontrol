from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin_delivered = fields.Float(compute='_compute_margin_delivered', store=True)
    margin_invoiced = fields.Float(compute='_compute_margin_invoiced', store=True)

    @api.depends('price_subtotal', 'qty_delivered', 'purchase_price')
    def _compute_margin_delivered(self):
        for line in self:
            price = (line.price_subtotal / line.product_uom_qty) if line.product_uom_qty else 0
            line.margin_delivered = price * line.qty_delivered - (line.purchase_price * line.qty_delivered)

    @api.depends('price_subtotal', 'qty_invoiced', 'purchase_price')
    def _compute_margin_invoiced(self):
        for line in self:
            price = (line.price_subtotal / line.product_uom_qty) if line.product_uom_qty else 0
            line.margin_invoiced = price * line.qty_invoiced - (line.purchase_price * line.qty_invoiced)
