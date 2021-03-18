# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        partner_id= self.env['res.partner'].browse(vals['partner_id'])
        if partner_id.vat == False:
            raise ValidationError(_("The user does not have a NIF"))
        elif partner_id.street == False or len(partner_id.state_id) == 0 or partner_id.zip == False or \
            len(partner_id.country_id) == 0:
            raise ValidationError(_("User does not have full address"))
        return super(AccountInvoice, self).create(vals)