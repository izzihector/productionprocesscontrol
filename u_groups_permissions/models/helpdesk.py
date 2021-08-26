# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def unlink(self):
        if self.env.user.has_group('u_groups_permissions.group_can_not_delete_ticket'):
            raise ValidationError(_('Error. You do not have permissions for delete tickets'))
        return super(HelpdeskTicket, self).unlink()


