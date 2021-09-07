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
    #internal_type = fields.Selection(related='account_id.internal_type', string="Internal Type", store=True, readonly=True)
