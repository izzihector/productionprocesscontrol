# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SaleOrderType(models.Model):
    _name = 'sale.order.type'

    name = fields.Char(
        'Name'
    )
    code = fields.Char(
        'Code'
    )
    order_id = fields.Many2one(
        'sale.order',
        'Order'
    )


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_existing_subscriptions(self):
        """
        Heredamos para evitar que al hacer confirm a la orden
        desde el generar factura de la subscripcion, se tengan
        que actualizar los valores
        """
        res = []
        if self.env.context.get('from_subscription', False):
            return res
        else:
            return super(SaleOrder, self).update_existing_subscriptions()

    def _prepare_subscription_data(self, template):
        res = super(SaleOrder, self)._prepare_subscription_data(template)

        periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
        invoicing_period = relativedelta(**{periods[template.recurring_rule_type]: template.recurring_interval})

        if template.recurring_rule_type == 'monthly':
            first_day = datetime.today().replace(day=1)
            recurring_next_date = first_day + invoicing_period
            res['recurring_next_date'] = recurring_next_date
        return res

    sale_order_type_id = fields.Many2one(
        'sale.order.type',
        'Type'
    )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #@api.multi
    def _timesheet_service_generation(self):
        res = super(SaleOrderLine, self)._timesheet_service_generation()
        for line in self:
            if line.project_id:
                subscription_line_id = self.env['sale.subscription.line'].\
                    search([('order_line_id', '=', line.id)])
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

    sale_order_type = fields.Many2one(
        'sale.order.type',
        'Type'
    )

    def _timesheet_create_task_prepare_values(self, project):
        record= super(SaleOrderLine, self)._timesheet_create_task_prepare_values(project)
        record['sales_hours']= record['planned_hours']
        return record