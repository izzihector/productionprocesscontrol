# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def create(self, vals):
        """
        It is inherited to prepare the message in the creation of the task.

        @param vals:
        """
        res = super(CrmLead, self).create(vals)
        if not res.date_closed and not vals.get('date_closed', False):
            res.date_closed = datetime.today() + relativedelta(months=+6)

        return res

    @api.onchange('partner_id')
    def onchange_partner_id_crm(self):
        for record in self:
            if record.partner_id:
                if record.partner_id.user_id:
                    record.user_id = record.partner_id.user_id.id