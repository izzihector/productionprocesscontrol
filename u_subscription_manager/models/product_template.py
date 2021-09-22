# -*- encoding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    show_product = fields.Boolean('Show product', help='The product will show up in tasks and tickets')
