# -*- encoding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import except_orm, ValidationError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    comercial_id = fields.Many2one(
        related="partner_id.user_id",
        store=True
    )

    
    