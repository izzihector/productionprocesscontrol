# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class SaleSubscriptionTemplate(models.Model):
    _inherit = 'sale.subscription.template'

    create_activity= fields.Many2one('res.users', string='Create activity for', required=True, help='user to whom the activity is assigned, when creating a subscription')