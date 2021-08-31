# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def unlink(self):
        if self.env.user.has_group('u_groups_permissions.group_can_not_delete_sale_order'):
            raise ValidationError(_('Error. You do not have permissions for delete sale orders'))
        return super(SaleOrder, self).unlink()


