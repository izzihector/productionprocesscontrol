# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TaskOportunityCreate(models.TransientModel):
    _name = "project.task.oportunity.wizard"
    _description = "Wizard project Task Creation"

    project_id = fields.Many2one('project.project')
    title = fields.Char()
    process_type = fields.Selection(
        [('normal', 'Normal'),('tech', 'Technical')],
        default='normal'
    )
    opportunity_id = fields.Many2one('crm.lead', default=lambda self: self.env.context.get('active_id'))
    project_allowed_ids = fields.Many2many('project.project', default=lambda self: self.env.user.company_id.project_allowed_ids.ids)

    def create_task(self):
        Task = self.env['project.task']
        for wizard in self:
            context = self.env.context.copy()
            title = wizard.process_type == 'normal' and 'Tarea Preventa: %s' % wizard.title or 'Consulta Técnica: %s' % wizard.title
            context.update({                
                'default_opportunity_id': context.get('active_id'),
                'default_project_id': wizard.project_id.id,
                'default_name': title
            })
            action = {
                'name': _('Task'),
                'view_mode': 'form',
                'res_model': 'project.task',
                'view_id': self.env.ref('project.view_task_form2').id,
                'type': 'ir.actions.act_window',
                'context': context,
            }
            return action