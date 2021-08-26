# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def write(self,values):
        res= super(ResPartner, self).write(values)
        if 'user_id' in values and values['user_id']:
            for record in self:
                if record.child_ids:
                    for child in record.child_ids:
                        child.user_id = values['user_id']
        return res

    nombre_fantasia= fields.Char(u'Nombre fantasía', help=u'Nombre fantasía', track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='Comercial', required=True,domain=[('share','=',False)], track_visibility='onchange')

