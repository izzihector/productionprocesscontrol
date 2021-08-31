# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from datetime import datetime


class project_task_add_description(models.TransientModel):
    _name = 'project.task.add.description'
    _description = 'Project Task Add Description'

    name = fields.Char(string='Task Add Description')
    description = fields.Html(required=True)

    def add_description(self):
        active_id = self.env.context.get('active_id', False)
        if active_id:
            task_id = self.env['project.task'].browse(active_id)
            user_id = self.env['res.users'].browse(self.env.context.get('uid', False))
            today_datetime = datetime.today()
            task_id.description += '<p>' + user_id.name + ' - ' + today_datetime.strftime("%d/%m/%Y - %H:%M:%S") + '</p>' + self.description
