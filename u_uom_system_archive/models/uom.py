# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import ValidationError


class UomUom(models.Model):
    _inherit = 'uom.uom'

    def write(self, vals):
        if 'active' in vals:
            if not self.env.user.has_group('base.group_system'):
                raise ValidationError(_('Error. Only a system manager can perform this action'))
        return super(UomUom, self).write(vals)