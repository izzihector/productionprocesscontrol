# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _, api
from odoo.exceptions import UserError
import pdb


class PCPlusProductividad(models.Model):
    _name = "pc.plus.productividad"
    _description = "Plus Productividad"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Plus Productividad')
    date = fields.Date(string='Fecha', required=True, track_visibility='always')
    employee_id = fields.Many2one('hr.employee', 'Empleado', required=True, track_visibility='always')
    amount = fields.Float(string='Importe', required=True, track_visibility='always')

    @api.model
    def create(self, vals):
        """
        It is inherited to prepare the message in the creation of the order.

        @param vals:
        """
        if not vals.get('amount'):
            raise UserError(_('Debe tener importe'))
        res = super(PCPlusProductividad, self).create(vals)
        content = ""
        content = content + "  \u2022 Fecha: " + res.date.strftime("%d/%m/%Y") + "<br/>"
        content = content + "  \u2022 Empleado: " + res.employee_id.name + "<br/>"
        content = content + "  \u2022 Importe: " + str(res.amount) + "<br/>"
        res.message_post(body=content)

        return res

    def write(self, values):
        if 'amount' in values and not values.get('amount'):
            raise UserError(_('Debe tener importe'))
        return super(PCPlusProductividad, self).write(values)
