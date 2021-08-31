# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PCContactLeads(models.TransientModel):
    _name = 'pc.contact.create.lead'

    campaign_id = fields.Many2one(comodel_name='utm.campaign', string=u'Campaña', required=True)

    def create_lead(self):
        """
        This function create a lead copying the data from a partner.
        """
        context = dict(self._context or {})
        partners = self.env['res.partner'].browse(context.get('active_ids'))
        crm_lead_obj = self.env['crm.lead']
        new_crm_ids = crm_lead_obj
        for partner in partners:
            new_crm = crm_lead_obj.create({
                'name': 'Masivo ' + partner.name,
                'type': 'lead',
                'partner_id': partner.id,
                'partner_name': partner.name,
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id.id if partner.state_id else False,
                'zip': partner.zip,
                'country_id': partner.country_id.id if partner.country_id else False,
                'website': partner.website,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'user_id': partner.user_id.id if partner.user_id else False,
                'campaign_id': self.campaign_id.id,
            })
            new_crm_ids += new_crm

        return {
            'domain': [('id', 'in', new_crm_ids.ids)],
            'name': 'Iniciativas',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'crm.lead',
            'view_id': False,
            'views': [(self.env.ref('crm.crm_case_tree_view_leads').id, 'tree'),
                      (self.env.ref('crm.crm_lead_view_form').id, 'form')],
            'type': 'ir.actions.act_window'
        }



