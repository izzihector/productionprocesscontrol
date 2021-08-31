# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _, api
from odoo.exceptions import UserError
from datetime import date
import pdb


class HrExpense(models.Model):
    _inherit = "hr.expense"
    _description = "Expense"

    expense_type_id = fields.Many2one('pc.hr.expense.type', string='Tipo de gasto', required=True,track_visibility='onchange')
    show_without_upload_photo = fields.Boolean()
    without_upload_photo = fields.Boolean()
    unit_amount = fields.Float("Importe", compute='_compute_from_product_id_company_id', store=True, required=True, copy=True,
        states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, digits = (16, 2))
    quantity = fields.Float(required=True, readonly=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, digits = (16, 2), default=1)

    @api.constrains('date')
    def _check_date(self):
        """
        Check if there is another expense with type 'Dieta' for the employee with the same date
        if that so raise Warning.
        """
        for rec in self:
            expense_type_obj = self.env['pc.hr.expense.type']
            expense_type_dieta = expense_type_obj.search([('name', 'like', 'Dieta')], limit=1)
            if expense_type_dieta and rec.expense_type_id == expense_type_dieta:
                expense_obj = self.env['hr.expense']
                expense = expense_obj.search([('employee_id', '=', rec.employee_id.id), ('expense_type_id', '=', rec.expense_type_id.id), ('date', '=', rec.date), ('id', '!=', rec.id)], limit=1)
                if expense:
                    raise UserError(_(
                        u"No se puede ingresar dos tipos de gasto 'Dieta' en un mismo día"))

    @api.constrains('unit_amount')
    def _check_unit_amount(self):
        """
        If the expense type is 'Dieta', the unit amount is more than expense type amount
        and the employee dont have diet_limitless raise Error.
        """
        for rec in self:
            expense_type_obj = self.env['pc.hr.expense.type']
            expense_type_dieta = expense_type_obj.search([('name', 'like', 'Dieta')], limit=1)
            if expense_type_dieta and rec.expense_type_id == expense_type_dieta and rec.unit_amount > expense_type_dieta.amount and not rec.employee_id.diet_limitless:
                raise UserError(_("Limite máximo de dieta 10 EUR al día"))

    @api.onchange('expense_type_id')
    def _onchange_expense_type_id(self):
        for rec in self:
            if rec.expense_type_id:
                rec.name=rec.expense_type_id.name
                rec.product_id = rec.expense_type_id.product_id.id
                rec.unit_amount = rec.expense_type_id.amount
            expense_type_obj = self.env['pc.hr.expense.type']
            expense_type_dieta = expense_type_obj.search([('name', 'like', 'Dieta')], limit=1)
            if expense_type_dieta and rec.expense_type_id == expense_type_dieta:
                rec.show_without_upload_photo = True

    @api.depends('product_id', 'company_id')
    def _compute_from_product_id_company_id(self):
        for expense in self.filtered('product_id'):
            expense = expense.with_company(expense.company_id)
            expense.name = expense.name or expense.product_id.display_name
            if not expense.attachment_number or (expense.attachment_number and not expense.unit_amount):
                expense.unit_amount = expense.product_id.price_compute('standard_price')[expense.product_id.id]
            if expense.expense_type_id:
                expense.unit_amount = expense.expense_type_id.amount
            expense.product_uom_id = expense.product_id.uom_id
            expense.tax_ids = expense.product_id.supplier_taxes_id.filtered(
                lambda tax: tax.company_id == expense.company_id)  # taxes only from the same company
            account = expense.product_id.product_tmpl_id._get_product_accounts()['expense']
            if account:
                expense.account_id = account


