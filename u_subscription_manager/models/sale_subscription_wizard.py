from odoo import models


class SaleSubscriptionWizard(models.TransientModel):
    _inherit = 'sale.subscription.wizard'

    def create_sale_order(self):
        res = super(SaleSubscriptionWizard, self).create_sale_order()
        order_id = res.get('res_id', False)
        order = self.env['sale.order'].browse(order_id)
        subscription_id = self.env['sale.subscription'].browse(self.env.context.get('active_id', False))
        if subscription_id:
            order.sub_template_id = subscription_id.template_id.id
        return res
