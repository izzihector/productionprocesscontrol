# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


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

    subscription_id = fields.Many2one(
        'sale.subscription',
        'Subscription'
    )
    sale_order_type_id = fields.Many2one(
        'sale.order.type',
        'Type'
    )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    project_id = fields.Many2one(
        'project.project',
        'Project'
    )
    cost = fields.Float(
        'Cost'
    )
    sale_order_type = fields.Many2one(
        'sale.order.type',
        'Type'
    )