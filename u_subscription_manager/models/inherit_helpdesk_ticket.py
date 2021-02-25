# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import except_orm, ValidationError

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    product_ticket = fields.One2many('product.ticket', 'ticket_id', string='Product ticket')
    product_ticket_total = fields.Float(compute='_compute_product_ticket_total', string="Total", store=True)
    information_date = fields.Datetime(string='Information date', default=fields.Datetime.now)

    @api.depends('product_ticket', 'product_ticket.quantity', 'product_ticket.price_subtotal')
    def _compute_product_ticket_total(self):
        for aux in self:
            aux.product_ticket_total = sum(line.price_subtotal for line in aux.product_ticket)
        return

    @api.model
    def create(self, vals_list):
        record = super(HelpdeskTicket, self).create(vals_list)
        self._create_line_ticket(record)
        return record

    def _create_line_ticket(self, record):
        partner_ids = record.partner_id + record.partner_id.parent_id + record.partner_id.child_ids
        list_subscription = self.env['sale.subscription'].search([('partner_id', 'in', partner_ids.mapped('id'))])

        line_subscription = list_subscription.mapped('recurring_invoice_line_ids')
        filter_line = line_subscription.filtered(lambda line: line.product_id.show_product == True)

        line_vals = []
        for line in filter_line:
            params = {
                'product_id': line.product_id.id,
                'sale_subscription_line_id': line.id,
            }
            line_vals.append((0, 0, params))
        record.update({
            'product_ticket': line_vals
        })
        return