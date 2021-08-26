# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #@api.multi
    def _create_analytic_account_process(self):
        for order in self:
            self.env['account.analytic.group'].check_sale_purchase_group()
            analytic_id = self.env['account.analytic.account'].search([
                ('partner_id', '=', order.partner_id.id),
                ('group_id.is_sale_purchase_group', '=', True)])
            if analytic_id:
                analytic_account_id = analytic_id[0]
            else:
                if order.partner_id.parent_id:
                    name = '%s + %s' % (order.partner_id.parent_id.name, 'compra-venta')
                    partner_id = order.partner_id.parent_id.id
                else:
                    name = '%s + %s' % (order.partner_id.name, 'compra-venta')
                    partner_id = order.partner_id.id

                analytic_account_id = self.env['account.analytic.account'].\
                    with_context(from_process=True).create({
                    'name': name,
                    'partner_id': partner_id,
                    'group_id': self.env['account.analytic.group'].search([
                        ('is_sale_purchase_group', '=', True)],
                        limit=1).id
                })
            order.analytic_account_id = analytic_account_id.id


    #@api.multi
    def _action_confirm(self):
        result = super(SaleOrder, self)._action_confirm()
        for order in self:
            if not order.analytic_account_id:
                order._create_analytic_account_process()
        return result