# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"

    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        lines = sale_orders.mapped('order_line').filtered(
            lambda l: l.display_type not in ['line_section', 'line_note'] and l.product_id.type != 'service' and l.purchase_price == 0
        )
        if lines:
            raise UserError(_("It has lines with zero cost."))
        return super().create_invoices()
