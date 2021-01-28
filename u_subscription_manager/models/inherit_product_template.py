# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import except_orm, ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    show_product= fields.Boolean('Show product', help='The product will show up in tasks and tickets')