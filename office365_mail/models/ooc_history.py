# -*- coding: utf-8 -*-
####################################################################
#
# © 2019-Today Somko Consulting (<https://www.somko.be>)
#
# License OPL-1 or later (https://www.odoo.com/documentation/user/11.0/legal/licenses/licenses.html)
#
####################################################################
from odoo import models, fields


class OocHistory(models.Model):
    _name = 'ooc.history'
    _description = "Outlook Connector History"

    mail = fields.Many2one('mail.message', string='Mail', required=True)
    #ondelete = 'cascade'
    model = fields.Char(related='mail.model', string='Model', store=True, readonly=False)
    res_id = fields.Many2oneReference(related='mail.res_id', string='Model Id', readonly=False)
    user = fields.Char(related='mail.author_id.name', string='User', store=True, readonly=False)
