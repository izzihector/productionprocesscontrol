# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _, api
from odoo.exceptions import UserError
import pdb


class HrExpenseType(models.Model):
    _name = "pc.hr.expense.type"
    _description = "Expense Type"

    name = fields.Char(string='Expense Type', required=True)
    amount = fields.Float(string='Importe', required=True)
    product_id = fields.Many2one('product.product', string='Product', tracking=True, required=True, domain="[('can_be_expensed', '=', True)]")

    @api.constrains('product_id')
    def _check_product_id(self):
        for rec in self:
            expense_type_obj = self.env['pc.hr.expense.type']
            expense_type = expense_type_obj.search([('product_id', '=', rec.product_id.id), ('id', '!=', rec.id)], limit=1)
            if expense_type:
                raise UserError(_("Expense type: %s has already this product, can't be two expense type with the same product." % expense_type.name))

    @api.model
    def create(self, values):
        if not values.get('amount'):
            raise UserError(_('Must have an amount'))
        return super(HrExpenseType, self).create(values)

    def write(self, values):
        if 'amount' in values and not values.get('amount'):
            raise UserError(_('Must have an amount'))
        return super(HrExpenseType, self).write(values)