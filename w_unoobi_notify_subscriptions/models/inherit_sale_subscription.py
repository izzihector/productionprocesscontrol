# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    @api.model
    def create(self, vals):
        record= super(SaleSubscription, self).create(vals)
        if len(record.template_id.create_activity) == 1:
            self._create_activity(record)
        return record

    def _create_activity(self, record):
        """
        create an activity for the responsible user in the subscription template
        :param record:
        :return:
        """
        assigned_user_id= record.template_id.create_activity
        obj_activity= self.env['mail.activity']
        obj_model= self.env['ir.model'].search([('model', '=', 'sale.subscription')])

        obj_activity.create({
            'activity_type_id': 4,
            'user_id': assigned_user_id.id,
            'summary': _('Subscription review'),
            'res_model_id': obj_model.id,
            'res_id': record.id
        })
        return