# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo13, Open Source Management Solution
#
############################################################################
from odoo.exceptions import ValidationError
from odoo import fields, models, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #@api.multi
    def action_confirm(self):
        record= super(SaleOrder, self).action_confirm()
        archived_products= self.order_line.filtered(lambda x: x.product_id.active == False and len(x.product_id) == 1)
        if len(archived_products) >= 1:
            raise ValidationError(_("The products {} are archived".format(archived_products.mapped('name'))))
        return record

    #@api.multi
    def action_invoice_create(self, grouped=False, final=False):
        for order in self:
            archived_products = order.order_line.filtered(lambda x: x.product_id.active == False and len(x.product_id) == 1)
            if len(archived_products) >= 1:
                raise ValidationError(_("The products {} are archived".format(archived_products.mapped('name'))))
        return super(SaleOrder, self).action_invoice_create()