from odoo import api, exceptions, fields, models, _
import pdb
from odoo.exceptions import UserError


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    _description = 'Activity'

    # This function control that an user can't change activities from another one.

    def write(self, values):
        if 'uid' in self._context:
            if self.user_id.id and self._context['uid'] != self.user_id.id:
                raise UserError(_("Can't modify an activity from another user"))
        return super(MailActivity, self).write(values)

    def unlink(self):
        if 'uid' in self._context:
            if self.user_id.id and self._context['uid'] != self.user_id.id:
                raise UserError(_("Can't modify an activity from another user"))
        return super(MailActivity, self).unlink()

    def _action_done(self, feedback=False, attachment_ids=None):
        if 'uid' in self._context:
            if self.user_id.id and self._context['uid'] != self.user_id.id:
                raise UserError(_("Can't modify an activity from another user"))
        return super(MailActivity, self)._action_done(feedback, attachment_ids)