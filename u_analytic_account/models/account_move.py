# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class AccountMove(models.Model):
    _inherit = 'account.move'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic account'
    )


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # TODO por ahora comentado hasta ver como afecta a las subscripciones, no deberia pero lo hace
    # TODO buscar otra manera
    # @api.model
    # def create(self, vals_list):
    #     res = super(AccountMoveLine, self).create(vals_list)
    #     move_id = self.env['account.move'].browse(vals_list.get('move_id', False))
    #     if move_id and move_id.analytic_account_id:
    #         if not vals_list.get('analytic_account_id', False):
    #             vals_list['analytic_account_id'] = move_id.analytic_account_id.id
    #     return res


