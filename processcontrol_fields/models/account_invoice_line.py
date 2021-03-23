# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    project_id = fields.Many2one('project.project', string='Proyecto', required=False)

    @api.model
    def create(self, vals):
        project_id = False
        try:
            if (vals['project_id']):
                project_id = vals['project_id']
        except:
            project_id = False

       # else:
            #raise exceptions.UserError(_("No se detecta origen"))

        invoice_lines = super(AccountInvoiceLine, self).create(vals)
        invoice_lines.write({'project_id': project_id})

        return invoice_lines