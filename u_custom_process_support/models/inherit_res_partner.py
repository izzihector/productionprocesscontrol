# -*- coding: utf-8 -*-

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    product_type_id = fields.Many2one(
        'product.type'
    )
    skype_check = fields.Boolean()