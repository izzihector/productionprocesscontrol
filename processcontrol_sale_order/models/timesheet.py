# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def unlink(self):
        for rec in self:
            user = rec._uid
            employee_id = self.env['hr.employee'].search([('user_id', '=', user)], limit=1)
            if rec.is_timesheet:
                if rec.employee_id.id != employee_id.id and not rec.env.user.has_group('processcontrol_sale_order.group_can_delete_timesheet'):
                    raise ValidationError(_('Error. No se puede eliminar una parte de hora de otro empleado'))
        return super(AccountAnalyticLine, self).unlink()


    @api.model
    def create(self, values):
        user = self._uid
        employee_id = self.env['hr.employee'].search([('user_id','=',user)],limit=1)
        if employee_id:
            if 'is_timesheet' in values and values['is_timesheet']:
                if 'employee_id' in values and values['employee_id'] != False:
                    if values['employee_id'] != employee_id.id and not rec.env.user.has_group('processcontrol_sale_order.group_can_delete_timesheet'):
                        raise ValidationError(_('Error. No se puede crear una parte de hora para otro empleado'))
        return super(AccountAnalyticLine, self).create(values)

    def write(self, values):
        for rec in self:
            user = rec._uid
            employee_id = self.env['hr.employee'].search([('user_id', '=', user)], limit=1)
            if rec.is_timesheet:
                if 'employee_id' in values and values['employee_id'] != False:
                    employee_to_modify_id = values['employee_id']
                else:
                    employee_to_modify_id=rec.employee_id.id
                if employee_to_modify_id != employee_id.id and not rec.env.user.has_group(
                        'processcontrol_sale_order.group_can_delete_timesheet'):
                    raise ValidationError(_('Error. No se puede modificar una parte de hora de otro empleado'))
        return super(AccountAnalyticLine, self).write(values)