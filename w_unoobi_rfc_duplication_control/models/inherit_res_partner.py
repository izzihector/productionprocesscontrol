# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import except_orm, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    #@api.one
    @api.constrains('vat')
    def _valid_rfc(self):
        if self.vat != False:
            query_vat = self.env['res.partner'].search([('vat', '=', self.vat), ('parent_id', '=', False), ('name', '!=', False)])
            if len(query_vat) >= 2:
                raise ValidationError(_('¡A user already has the same RFC!'))
        return