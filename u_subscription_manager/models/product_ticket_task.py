# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import except_orm, ValidationError

class ProductTicketTask(models.Model):
    _name = 'product.ticket.task'

    name= fields.Char('Name')
    sale_subscription_id = fields.Many2one('sale.subscription', string='Subscription', required=True, ondelete='cascade', index=True, copy=False)
    sale_subscription_line_id = fields.Many2one('sale.subscription.line', string='Subscription line', required=True, ondelete='cascade', index=True, copy=False)
    product_id= fields.Many2one('product.product', string='Product')
    #description= fields.Char(string='Description', related='sale_subscription_line_id.name')
    cost= fields.Float(string='Cost', related='sale_subscription_line_id.cost')
    quantity= fields.Float(string='Quantity', related='sale_subscription_line_id.quantity')
    umo_id= fields.Many2one('uom.uom', string='Unit of measurement', related='sale_subscription_line_id.uom_id')
    price_unit= fields.Float(string='Unit price', related='sale_subscription_line_id.price_unit')
    price_subtotal= fields.Float(string='Subtotal', related='sale_subscription_line_id.price_subtotal')
