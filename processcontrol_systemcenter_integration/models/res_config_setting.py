# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    key_produccion = fields.Char(string="WS Producción")
    user = fields.Char(string="Usuario")
    password = fields.Char(string=u'Contraseña')

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(key_produccion=self.env['ir.config_parameter'].sudo().get_param('processcontrol_systemcenter_integration.key_produccion'))
        res.update(key_testing=self.env['ir.config_parameter'].sudo().get_param('processcontrol_systemcenter_integration.user'))
        res.update(system_id=self.env['ir.config_parameter'].sudo().get_param('processcontrol_systemcenter_integration.password'))
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('processcontrol_systemcenter_integration.key_produccion', self.key_produccion)
        self.env['ir.config_parameter'].sudo().set_param('processcontrol_systemcenter_integration.user', self.user)
        self.env['ir.config_parameter'].sudo().set_param('processcontrol_systemcenter_integration.password', self.password)
        return True