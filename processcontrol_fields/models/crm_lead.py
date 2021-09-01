# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
	_inherit = 'crm.lead'

	#@api.multi
	def create_ticket(self):
		return{
			'name': _('Crear Ticket'),
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'project.task',
	}
