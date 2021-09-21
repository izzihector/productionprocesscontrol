import time

from odoo import api, fields, models, SUPERUSER_ID


class AccountAnalyticLine(models.Model):
    _name = 'account.analytic.line'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'account.analytic.line']
    _order = 'date desc, id desc'
    name = fields.Char(tracking=True)
    date = fields.Date(tracking=True)
    unit_amount = fields.Monetary(tracking=True)
    task_id = fields.Many2one(tracking=True)
    project_id = fields.Many2one(tracking=True)
    negative = fields.Boolean('Negativo', tracking=True)
    changes = fields.Integer('Cambios', compute='_count_changes', store=True, default=None)
    need_check = fields.Boolean('Pendiente de verificación', default=False)

    def action_verify(self):
        for record in self:
            record.need_check = False
            record.message_post(body='Cambios verificados')
            record.changes = 0

    def action_clean(self):
        for record in self:
            ids = record.message_ids.filtered(lambda x: x.tracking_value_ids).ids
            record.update({'message_ids': [(2, _id, 0) for _id in ids]})
            record.message_post(body='Historial de cambios eliminado')

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        res = self
        for val in vals_list:
            self._compute_negative(val)
            res += super(AccountAnalyticLine, self).create([val])
        return res

    def write(self, vals):
        self._compute_negative(vals)
        return super(AccountAnalyticLine, self).write(vals)

    def _compute_negative(self, values):
        # Obtenemos los tiempos disponibles desde la tarea
        task = self.env['project.task'].browse([values.get('task_id', self.task_id.id)])
        available = min(task.remaining_hours, task.available_hour)

        # Se marca como negativo si tiene tiempo y supera el disponible
        if values.get('unit_amount') and available + self.unit_amount - values['unit_amount'] < 0:
            values['negative'] = True
            values['need_check'] = True

    @api.depends('message_ids')
    def _count_changes(self):
        """
        Contamos el número de veces que se ha editdo modificando algun campo trackeado
        :return:
        """
        for record in self:
            changes = len(record.message_ids.filtered(lambda x: x.tracking_value_ids))
            if changes > record.changes and self.env.uid != SUPERUSER_ID and not self.env.user.has_group(
                        'hr_timesheet.group_hr_timesheet_approver'):
                record.need_check = True
            record.with_user(record.employee_id).changes = changes
