# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrderType(models.Model):
    _name = 'sale.order.type'
    _description = 'sale.order.type'

    name = fields.Char('Name')
    code = fields.Char('Code')
    order_id = fields.Many2one( 'sale.order','Order')

