# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import except_orm, ValidationError

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    timecheet_unit_amount = fields.Float(compute='_compute_timesheet_ticket_total', string="Total", store=False)
  
    @api.depends('timesheet_ids', 'timesheet_ids.unit_amount')
    def _compute_timesheet_ticket_total(self):
        for aux in self:
            aux.timecheet_unit_amount = sum(line.unit_amount for line in aux.timesheet_ids) 
        return

    
    