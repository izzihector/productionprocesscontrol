# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = ['account.invoice']

    numero_factura_sage = fields.Char(
        string='Numero Factura Sage',
        required=False)

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice, self).create(vals)
        payterm = False
        str = "SUB"

        if (str in invoice.origin):
            SSL = self.env['sale.subscription']
            suscripciones = SSL.search([('name', '=', invoice.origin)])

            if (suscripciones):
                for sub in suscripciones:
                    payterm = sub.termino_pago
                    idSubscription = sub.id
                    nombreSuscripcion = sub.name

                    invoice.write({'payment_term_id': payterm.id})

        return invoice