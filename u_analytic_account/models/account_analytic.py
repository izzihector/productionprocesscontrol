# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields,_
from odoo.exceptions import ValidationError


class AccountAnalyticGroup(models.Model):
    _inherit = 'account.analytic.group'

    @api.model
    def check_sale_purchase_group(self):
        sale_purchase_group = self.search([('is_sale_purchase_group', '=', True)])
        if not sale_purchase_group:
            raise ValidationError(_('Error. A analytic group  must be defined as Sale-Purchase group'))

    is_sale_purchase_group = fields.Boolean(
        'Is sale-purchase group'
    )


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    #@api.multi
    def name_get(self):
        res = []
        for analytic in self:
            name = analytic.name
            if analytic.code:
                name = '[' + analytic.code + '] ' + name
            if analytic.partner_id.commercial_partner_id.name:
                name = name + ' - ' + analytic.partner_id.commercial_partner_id.name
            if analytic.group_id and analytic.group_id.is_sale_purchase_group:
                name = '%s + Compra-Venta' % analytic.partner_id.name
            res.append((analytic.id, name))
        return res