# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductType(models.Model):
    _name = "product.type"
    _description = "Process Product Type"

    name = fields.Char(string='Description')
    code = fields.Char(string='Code')
