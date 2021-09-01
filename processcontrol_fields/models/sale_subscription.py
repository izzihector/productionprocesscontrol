# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import UserError, ValidationError


class AccountInvoice(models.Model):
    _inherit = 'sale.subscription'

    termino_pago = fields.Many2one('account.payment.term', string='Terminos de Pago', required=False)
