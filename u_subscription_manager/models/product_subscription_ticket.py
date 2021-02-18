# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import except_orm, ValidationError

class ProductSubscription(models.Model):
    _name = 'product.subscription'

    name= fields.Char('Name')
    task_id = fields.Many2one('project.task', string='Task', required=True, ondelete='cascade', index=True, copy=False)
    sale_subscription_line_id = fields.Many2one('sale.subscription.line', string='Subscription line', required=True, ondelete='cascade', index=True, copy=False)
    product_id= fields.Many2one('product.product', string='Product')
    subscription_id = fields.Many2one('sale.subscription', string='Subscription', related='sale_subscription_line_id.analytic_account_id')
    quantity= fields.Float(string='Quantity', related='sale_subscription_line_id.quantity')
    umo_id= fields.Many2one('uom.uom', string='Unit of measurement', related='sale_subscription_line_id.uom_id')
    price_unit= fields.Float(string='Unit price', related='sale_subscription_line_id.price_unit')
    price_subtotal= fields.Float(string='Subtotal', related='sale_subscription_line_id.price_subtotal')
    description_sale_subscription_line= fields.Text(related='sale_subscription_line_id.name', string='Description')


class ProductTicket(models.Model):
    _inherit = 'product.subscription'
    _name = 'product.ticket'

    #El campo 'task_id' no es requerido en este modelo
    task_id = fields.Many2one('project.task', string='Task', required=False, ondelete='cascade', index=True, copy=False)
    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket', required=True, ondelete='cascade', index=True, copy=False)