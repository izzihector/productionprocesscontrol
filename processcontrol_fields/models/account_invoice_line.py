# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError


class AccountInvoiceLine(models.Model):
    _inherit = ['account.invoice.line']

    project_id = fields.Many2one('project.project', string='Proyecto', required=False)

    @api.model
    def create(self, vals):
        raise exceptions.UserError(_(vals))

        project_id = vals['x_studio_proyecto_pedido_venta']
        invoice_lines = super(AccountInvoiceLine, self).create(vals)
        invoice_lines.write({'project_id': project_id})

        return invoice_lines