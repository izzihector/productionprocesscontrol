# -*- coding: utf-8 -*-
####################################################################
#
# © 2019-Today Somko Consulting (<https://www.somko.be>)
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/11.0/legal/licenses/licenses.html)
#
####################################################################
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OocMessageModel(models.Model):
    _name = 'ooc.message.model'
    _description = "Odoo Outlook Connector Message Model"

    name = fields.Char(string="Display Name", required=True, translate=True, help="This is the name of the model that the user will see in Outlook")
    model_id = fields.Many2one('ir.model', string='Model', required=True, ondelete='cascade', help="The Odoo model to which you want to be able to attach emails")
    model = fields.Char(related='model_id.model', store=True, readonly=False)

    auto_select = fields.Boolean(string="Auto Select Item", help="Automatically select a match in the Outlook Add-In, based on a domain filter", default=False)
    filter_regex = fields.Char(string="Filter Regex", help="For example: (SL.?\d{4}(.?\d{3})?)")
    filter_domain = fields.Char(string="Filter Domain", help="For example: [['name', 'ilike', match[0].replace(' ', '-')]]")

    auto_filter = fields.Boolean(string="Auto Filter Item", help="Automatically proposes matches in the Outlook Add-In, based on a domain filter. If no matches are found, then outlook will propose all records", default=False)
    select_domain = fields.Char(string="Select Domain", help="For example: ['|', '|', '|', ['partner_id.email', '=',  sender_email], ['email_from','=', sender_email], ['partner_id.name', '=',  sender_name], ['contact_name', '=', sender_name]]")

    default = fields.Boolean(string="Selected by Default", help="This model is the default selected object in the Outlook Add-In", default=False)

    # ------------
    #  Constraint
    # ------------
    @api.constrains('default')
    def constraint_default(self):
        if self.default and self.search_count([('default', '=', True)]) > 1:
            raise ValidationError(_('Can only set one model as default!'))

    # ---------
    #  Helpers
    # ---------
    @api.model
    def get_allowed_models(self):
        sr_models = self.search_read()
        allowed_models = []

        for sr_m in sr_models:
            try:
                self.env[sr_m['model']].check_access_rights('read')

                allowed_models.append({'name': sr_m['name'], 'model': sr_m['model'], 'default': sr_m['default']})
            except:
                pass

        return allowed_models

    @api.model
    def get_allowed_items(self, params):
        fields = ['id', 'display_name', 'name']
        is_project = False
        domain = [('name', 'ilike', params['search'])]
        message_obj = self.search([('model', '=', params['model'])], limit=1)

        if params['model'] == 'project.project':
            fields.append('privacy_visibility')
            fields.append('message_is_follower')
            is_project = True

        if len(self.env['ir.model.fields'].search([('model', '=', params['model']), ('name', '=', 'display_name'), ('store', '=', True)])):
            domain = [('display_name', 'ilike', params['search'])]

        self.search([('model', '=', params['model'])], limit=1)

        sr_items = []

        # Filter based on user email, etc.
        if message_obj.auto_filter:
            sender_domain = eval(message_obj.select_domain, {
                'sender_name': params['send_name'],
                'sender_email': params['send_mail'],
            }) + domain
            sr_items = self.env[params['model']].search_read(sender_domain , fields, limit=10)

        # Fallback to default search if no matches have been found
        if not sr_items:
            sr_items = self.env[params['model']].search_read(domain, fields, limit=10)

        # Add autoselect item
        auto_select = self.get_auto_select_item(params)
        sr_items += self.env[params['model']].search_read([('id', '=', auto_select.id)], fields)

        allowed_items = []

        for sr_i in sr_items:
            if is_project:
                # if sr_i['privacy_visibility'] != 'employees':
                if not sr_i['message_is_follower']:
                    continue

                del sr_i['privacy_visibility']
                del sr_i['message_is_follower']

            if sr_i['id'] == auto_select.id:
                sr_i['default'] = True

            allowed_items.append(sr_i)

        return allowed_items

    @api.model
    def get_auto_select_item(self, params):
        message_obj = self.search([('model', '=', params['model'])], limit=1)
        model_obj = self.env[params['model']]

        if message_obj.auto_select and 'title' in params and params['title']:
            matches = re.findall(message_obj.filter_regex, params['title'])

            if matches:
                # Match gets used in eval, maybe make this save
                match = matches[0]
                results = model_obj.search(eval(message_obj.filter_domain))

                if len(results) == 1:
                    return results

        return model_obj
