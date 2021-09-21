from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    # margin_delivered = fields.Float('Margin (Delivered)', readonly=True)
    margin_invoiced = fields.Float('Margin (Invoiced)', readonly=True)

    # product_uom_qty_uor = fields.Float('Qty Ordered (Reference)', readonly=True)
    # qty_delivered_uor = fields.Float('Qty Delivered (Reference)', readonly=True)
    # qty_to_invoice_uor = fields.Float('Qty To Invoice (Reference)', readonly=True)
    # qty_invoiced_uor = fields.Float('Qty Invoiced (Reference)', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['margin_invoiced'] = ", SUM(l.margin_invoiced / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 " \
                                    "ELSE s.currency_rate END) AS margin_invoiced\n"

        '''fields['margin_delivered'] = ", SUM(l.margin_delivered / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 " \
                                     "ELSE s.currency_rate END) AS margin_delivered\n"
        fields['product_uom_qty_uor'] = ", CASE WHEN l.product_id IS NOT NULL THEN sum(product_uom_qty / u2.factor) " \
                                        "ELSE 0 END as product_uom_qty_uor\n"
        fields['qty_delivered_uor'] = ", CASE WHEN l.product_id IS NOT NULL THEN sum(qty_delivered / u2.factor) " \
                                      "ELSE 0 END as qty_delivered_uor\n"
        fields['qty_to_invoice_uor'] = ", CASE WHEN l.product_id IS NOT NULL THEN sum(qty_to_invoice / u2.factor) " \
                                       "ELSE 0 END as qty_to_invoice_uor\n"
        fields['qty_invoiced_uor'] = ", CASE WHEN l.product_id IS NOT NULL THEN sum(qty_invoiced / u2.factor) " \
                                     "ELSE 0 END as qty_invoiced_uor\n"'''

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
