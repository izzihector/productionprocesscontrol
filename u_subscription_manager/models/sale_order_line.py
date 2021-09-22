from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    sale_order_type = fields.Many2one('sale.order.type', 'Type')

    def _timesheet_service_generation(self):
        super(SaleOrderLine, self)._timesheet_service_generation()
        for line in self:
            if line.project_id:
                subscription_line_id = self.env['sale.subscription.line'].search([('order_line_id', '=', line.id)])
                if subscription_line_id:
                    subscription_line_id.project_id = line.project_id.id

    def _prepare_subscription_line_data(self):
        res = super(SaleOrderLine, self)._prepare_subscription_line_data()
        for index, line in enumerate(res):
            line[2].update({
                'order_line_id': self[index].id,
                'cost': self[index].purchase_price
            })
        return res

    def _timesheet_create_task_prepare_values(self, project):
        record = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(project)
        record['sales_hours'] = record['planned_hours']
        return record

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
