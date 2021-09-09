# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def unlink(self):
        for rec in self:
            if rec.is_timesheet:
                if not rec.env.user.has_group('processcontrol_sale_order.group_can_delete_timesheet'):
                    raise ValidationError(_('Error. No tienes el permiso para poder eliminar una parte de hora'))
        return super(AccountAnalyticLine, self).unlink()

    cliente_id = fields.Many2one('helpdesk_ticket_id.partner_id.parent_id','res.partner',string='Cliente del ticket',store=True)
