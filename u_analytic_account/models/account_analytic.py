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

    @api.depends('name')
    def name_get(self):
        result = []
        for account in self:
            if account.group_id and account.group_id.is_sale_purchase_group:
                name = '%s + Compra-Venta' % account.partner_id.name
                result.append((account.id, name))
                return result
            else:
                return super(AccountAnalyticAccount, self).name_get()