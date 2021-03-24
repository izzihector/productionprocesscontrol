# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    #@api.multi
    def create_ticket(self):
        return {
            'name': _('Nueva Gestión'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.task',
        }
