from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    sub_template_id = fields.Many2one(comodel_name='sale.subscription.template',string=u'Plantilla de suscripción', readonly=True)
    sale_order_type_id = fields.Many2one(comodel_name='sale.order.type',string='Tipo',readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['sub_template_id'] = ", s.sub_template_id as sub_template_id"
        fields['sale_order_type_id'] = ", s.sale_order_type_id as sale_order_type_id"

        groupby += ', s.sub_template_id,s.sale_order_type_id'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
