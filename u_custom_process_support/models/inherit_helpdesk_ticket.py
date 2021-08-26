# -*- encoding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import except_orm, ValidationError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _notify_customer(self):
        self.ensure_one()
        # Enviar correo con aceptar o rechazar
        mail_template = self.env.ref('u_custom_process_support.email_template_edi_notify_unproduct_type')
        mail_template.send_mail(self.id, force_send=True)

    @api.model
    def create(self, vals):
        res = super().create(vals)
        partner_id = res.partner_id
        parent_id = partner_id.parent_id
        parent_sucess = True
        if parent_id and not parent_id.skype_check and not parent_id.product_type_id:
            parent_sucess = False
        if partner_id and not partner_id.skype_check and not partner_id.product_type_id or not parent_sucess:
            res.kanban_state = 'blocked'
            res._notify_customer()
        return res