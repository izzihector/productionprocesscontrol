# -*- encoding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    description = fields.Char('Description', help='The description will be concatenated to create the project name')
