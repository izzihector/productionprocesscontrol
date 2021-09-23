# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    numero_factura_sage = fields.Char()

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Comento este field porque no se utiliza y está duplicado con 'account_internal_type' mostrando un warning
    # TODO: Comprobar, ¿eliminar clase?
    user_type_id = fields.Many2one(related='account_id.user_type_id', string="Tipo de cuenta", store=True, readonly=True)
    invoice_user_id = fields.Many2one(related='move_id.invoice_user_id',string='Comercial',store=True)
