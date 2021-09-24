from odoo import api, exceptions, fields, models, _
import pdb
from odoo.exceptions import UserError


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    _description = 'Activity'


    def _action_done(self, feedback=False, attachment_ids=None):
        if 'uid' in self._context:
            if self.user_id.id and self._context['uid'] != self.user_id.id:
                raise UserError(_("No se puede marcar como hecho la actividad de otra persona"))
        return super(MailActivity, self)._action_done(feedback, attachment_ids)
    

    def unlink(self):
        for activity in self:
            if 'uid' in activity._context:
                if activity.user_id.id and activity._context['uid'] != activity.user_id.id:
                    raise UserError(_("No se puede cancelar la actividad de otra persona"))
        return super(MailActivity, self).unlink()
