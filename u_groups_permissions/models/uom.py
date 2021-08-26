# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import ValidationError


class UomUom(models.Model):
    _inherit = 'uom.uom'

    def write(self, vals):
        if 'active' in vals:
            if self.env.user.has_group('u_groups_permissions.group_can_not_archive_uom'):
                raise ValidationError(_('Error. You do not have permissions for archive UoMs'))
        return super(UomUom, self).write(vals)

    def unlink(self):
        if self.env.user.has_group('u_groups_permissions.group_can_not_delete_uom'):
            raise ValidationError(_('Error. You do not have permissions for delete UoMs'))
        return super(UomUom, self).unlink()

    @api.model
    def create(self, vals_list):
        if self.env.user.has_group('u_groups_permissions.group_can_not_create_uom'):
            raise ValidationError(_('Error. You do not have permissions for create UoMs'))
        return super(UomUom, self).create(vals_list)