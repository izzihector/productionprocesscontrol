from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin_delivered = fields.Float(compute='_compute_margin_delivered', store=True)
    margin_invoiced = fields.Float(compute='_compute_margin_invoiced', store=True)

    @api.depends('price_unit', 'qty_delivered', 'purchase_price', 'product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_margin_delivered(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price,
                line.order_id.currency_id,
                line.line.qty_delivered,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id
            )
            line.margin_delivered = taxes['total_excluded'] * line.qty_delivered - \
                                    (line.purchase_price * line.qty_delivered)

    @api.depends('price_unit', 'qty_invoiced', 'purchase_price', 'product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_margin_invoiced(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price,
                line.order_id.currency_id,
                line.line.qty_invoiced,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id
            )

            line.margin_invoiced = taxes['total_excluded'] * line.qty_invoiced - \
                                   (line.purchase_price * line.qty_invoiced)
