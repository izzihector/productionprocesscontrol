# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = ['account.invoice']

    numero_factura_sage = fields.Char(
        string='Numero Factura Sage',
        required=False)
