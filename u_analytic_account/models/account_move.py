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

    @api.model
    def create(self, vals_list):
        res = super(AccountMove, self).create(vals_list)
        if res.move_type == 'in_invoice' and res.analytic_account_id:
            for line in res.invoice_line_ids:
                # Respetamos el valor si se define a mano
                if not line.analytic_account_id:
                    line.analytic_account_id = res.analytic_account_id.id
        return res



