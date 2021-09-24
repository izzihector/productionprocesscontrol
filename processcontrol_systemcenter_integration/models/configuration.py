
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SystemCenterProductConfiguration(models.Model):
    _name = 'product.configuration.system.center'

    product_id = fields.Many2one(comodel_name='product.product',string='Producto Odoo',required=True)
    code = fields.Char(string=u'Código en SC',required=True)

    _sql_constraints = [
        ('code_product_uniq', 'unique(code,product_id)',u'Ya existe ese código y producto configurado')
    ]

