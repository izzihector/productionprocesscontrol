from odoo import models, fields


class SaleSubscriptionTemplate(models.Model):
    _inherit = 'sale.subscription.template'

    payment_mode = fields.Selection(
        selection_add=[('quotation_sale_order', "Quotation"),
                       ('confirmed_sale_order', 'Confirmed Sale Order')],
        ondelete={'quotation_sale_order': 'set default', 'confirmed_sale_order': 'set default'}
    )
    sale_order_type_id = fields.Many2one('sale.order.type', 'Sale order type')
