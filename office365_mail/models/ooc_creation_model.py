# -*- coding: utf-8 -*-
####################################################################
#
# © 2019-Today Somko Consulting (<https://www.somko.be>)
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/11.0/legal/licenses/licenses.html)
#
####################################################################
from odoo import models, fields, api


class OocCreationModel(models.Model):
    _name = 'ooc.creation.model'
    _description = "Odoo Outlook Connector Creation Model"

    name = fields.Char(string="Name", required=True, translate=True, help="This is the name of the model that the user will see in Outlook")
    model_id = fields.Many2one('ir.model', string='Model', required=True, ondelete='cascade', help="The model that you want to be able to create from an Outlook Email")
    model_name = fields.Char(related='model_id.model', store=True, readonly=False)

    subject_field_title = fields.Char(string="Subject Field Title", translate=True, help="This is the label of the subject field that the user will see in Outlook")
    subject_field_id = fields.Many2one('ir.model.fields', string='Subject field', required=True, ondelete='cascade', help="The field in which the subject of the email will be stored in the newly created record")
    subject_field_name = fields.Char(related='subject_field_id.name', store=True, readonly=False)

    message_field_title = fields.Char(string="Message Field Title", translate=True, help="This is the label of the message body field that the user will see in Outlook")
    message_field_id = fields.Many2one('ir.model.fields', string='Message field', required=True, ondelete='cascade', help="The field in which the message of the email will be stored in the newly created record")
    message_field_name = fields.Char(related='message_field_id.name', store=True, readonly=False)
    message_field_type = fields.Selection(related='message_field_id.ttype', readonly=False)

    from_email_field_id = fields.Many2one('ir.model.fields', string='From Email field', help="The field in which the email address of the sender of the email will be stored in the newly created record")
    from_email_field_name = fields.Char(related='from_email_field_id.name', store=True, readonly=False)

    from_name_field_id = fields.Many2one('ir.model.fields', string='From Name field', help="The field in which the name of the sender of the mail will be stored in the newly created record")
    from_name_field_name = fields.Char(related='from_name_field_id.name', store=True, readonly=False)

    user_field_id = fields.Many2one('ir.model.fields', string='User', help="The field in which the user of the Outlook Add-In will be stored in the newly created record")
    user_field_name = fields.Char(related='user_field_id.name', store=True, readonly=False)

    @api.model
    def get_allowed_models(self):
        sr_models = self.search_read()
        allowed_models = []

        for sr_m in sr_models:
            try:
                self.env[sr_m['model_name']].check_access_rights('create')

                allowed_models.append(sr_m)
            except:
                pass

        return allowed_models
