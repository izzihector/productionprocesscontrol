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

    @api.constrains('partner_id','move_type')
    def check_partner_id_information(self):
        if self.move_type:
            if self.move_type in ('in_invoice','out_invoice'):
                if self.partner_id:
                    if not self.partner_id.vat:
                        raise ValidationError(_("The user does not have a NIF"))
                    if not self.partner_id.street or not self.partner_id.state_id or not self.partner_id.zip or not self.partner_id.country_id:
                        raise ValidationError(_("User does not have full address"))
