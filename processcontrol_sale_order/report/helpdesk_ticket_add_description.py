# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from datetime import datetime


class HelpdeskTicketAddDescription(models.TransientModel):
    _name = 'helpdesk.ticket.add.description'
    _description = 'Helpdesk Ticket Add Description'

    name = fields.Char(string='Ticket Add Description')
    description = fields.Text(required=True)

    def add_description(self):
        active_id = self.env.context.get('active_id', False)
        if active_id:
            ticket_id = self.env['helpdesk.ticket'].browse(active_id)
            user_id = self.env['res.users'].browse(self.env.context.get('uid', False))
            today_datetime = datetime.today()
            if ticket_id.description:
                ticket_id.description += '\n' + user_id.name + ' - ' + today_datetime.strftime(
                    "%d/%m/%Y - %H:%M:%S") + '\n' + self.description
            else:
                ticket_id.description = user_id.name + ' - ' + today_datetime.strftime(
                    "%d/%m/%Y - %H:%M:%S") + '\n' + self.description
