# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.tools.misc import get_lang

_logger = logging.getLogger(__name__)

MAPPED_RATES = {
    1: 1,
    5: 3,
    10: 5,
}

class TicketsProcess(http.Controller):

    @http.route('/tickets/<string:token>/accept/<int:ticket_id>', type='http', auth="public", website=True)
    def accept_tickets(self, token, ticket_id, **kwargs):
        
        ticket_obj = request.env['helpdesk.ticket'].sudo().search([('access_token', '=', token)])
        if not ticket_obj:
            return request.not_found()
        current_stage = ticket_obj.stage_id
        next_state = request.env['helpdesk.stage'].search(
            [
                ('team_ids', 'in', ticket_obj.team_id.id),
                ('sequence', '>', current_stage.sequence)
            ], 
            order='sequence',
            limit=1
        )
        ticket_obj.write(
            {
                'stage_id': next_state.id,
                'kanban_state': 'done'
            }
        )
      
    @http.route('/tickets/<string:token>/reject/<int:ticket_id>', type='http', auth="public", website=True)
    def reject_tickets(self, token, ticket_id, **kwargs):
        ticket_obj = request.env['helpdesk.ticket'].sudo().search([('access_token', '=', token)])
        if not ticket_obj:
            return request.not_found()
        close = ticket_obj.team_id._get_closing_stage()
        ticket_obj.write(
            {
                'stage_id': close.id
            }
        )
