# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _, api, fields
from odoo.exceptions import UserError


class Task(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        """
        It is inherited to prepare the message in the creation of the task.

        @param vals:
        """
        res = super(Task, self).create(vals)
        content = ""
        if vals.get('timesheet_ids', False):
            content += "Parte de Horas: <br/>"
            for ts in vals.get('timesheet_ids'):
                if content != "Parte de Horas: <br/>":
                    content += "------------------------------------------------------------------------------<br/>"
                for field_name in ts[2]:
                    new_val = ts[2][field_name]
                    if field_name == 'date':
                        content += "  \u2022 Fecha: " + new_val + "<br/>"
                    elif field_name == 'employee_id':
                        new_employee = self.env['hr.employee'].browse(new_val).name
                        content += "  \u2022 Empleado: " + new_employee + "<br/>"
                    elif field_name == 'unit_amount':
                        content += "  \u2022 Duración: " + '{0:02.0f}:{1:02.0f}'.format(
                            *divmod(new_val * 60, 60)) + "<br/>"
                    elif field_name == 'name' and new_val:
                        content += "  \u2022 Descripción: " + new_val + "<br/>"
        res.message_post(body=content)

        return res

    def write(self, values):
        content = ""
        # Tracking if time sheet is changed
        if 'timesheet_ids' in values:
            aal_obj = self.env['account.analytic.line']
            content += "Parte de Horas: <br/>"
            for ts in values['timesheet_ids']:
                if ts[0] == 0:
                    if content != "Parte de Horas: <br/>":
                        content += "------------------------------------------------------------------------------<br/>"
                    for change_vals in ts[2]:
                        new_val = ts[2][change_vals]
                        if change_vals == 'date':
                            content += "  \u2022 Fecha: " + new_val + "<br/>"
                        elif change_vals == 'employee_id':
                            new_employee = self.env['hr.employee'].browse(new_val).name
                            content += "  \u2022 Empleado: " + new_employee + "<br/>"
                        elif change_vals == 'unit_amount':
                            content += "  \u2022 Descripción: " + '{0:02.0f}:{1:02.0f}'.format(*divmod(new_val * 60, 60)) + "<br/>"
                        elif change_vals == 'name' and new_val:
                            content += "  \u2022 Descripción: " + new_val + "<br/>"
                elif ts[0] == 2:
                    if content != "Parte de Horas: <br/>":
                        content += "------------------------------------------------------------------------------<br/>"
                    unlinked_aal = aal_obj.browse(ts[1])
                    content += "  \u2022 Elimino la parte de hora %s de %s horas<br/>" % \
                               (unlinked_aal.name, '{0:02.0f}:{1:02.0f}'.format(*divmod(unlinked_aal.unit_amount * 60, 60)))
                elif ts[0] == 1:
                    if content != "Parte de Horas: <br/>":
                        content += "------------------------------------------------------------------------------<br/>"
                    aal_changed = aal_obj.browse(ts[1])
                    for change_vals in ts[2]:
                        new_val = ts[2][change_vals]
                        if change_vals == 'date':
                            content += "  \u2022 Fecha: " + aal_changed.date.strftime("%d/%m/%Y") + "&#8594;" + new_val + "<br/>"
                        elif change_vals == 'employee_id':
                            new_employee = self.env['hr.employee'].browse(new_val).name
                            content += "  \u2022 Empleado: " + aal_changed.employee_id.name + "&#8594;" + new_employee + "<br/>"
                        elif change_vals == 'name':
                            content += "  \u2022 Descripción: " + aal_changed.name + "&#8594;" + (new_val if new_val else ' ') + "<br/>"
                        elif change_vals == 'unit_amount':
                            content += "  \u2022 Duración: " + '{0:02.0f}:{1:02.0f}'.format(*divmod(aal_changed.unit_amount * 60, 60))\
                                       + "&#8594;" + '{0:02.0f}:{1:02.0f}'.format(*divmod(new_val * 60, 60)) + "<br/>"

        if content == "Parte de Horas: <br/>":
            content = ''
        if self:
            self.message_post(body=content)
        return super(Task, self).write(values)

    def _compute_total_sale_hour(self):
        for task in self:
            total_sh = 0
            sol_obj = self.env['sale.order.line']
            if task.project_id:
                project_sol = sol_obj.search([('project_id', '=', task.project_id.id)])
                for sol in project_sol:
                    if sol.product_uom:
                        if 'hora' in sol.product_uom.name:
                            total_sh += float(
                                sol.product_uom.name.rsplit(' hora')[0].replace(',', '.')) * sol.qty_invoiced
                        else:
                            total_sh += sol.qty_invoiced
            task.total_sale_hour = total_sh

    def _compute_total_work_hour(self):
        for task in self:
            total_wh = 0
            aal_obj = self.env['account.analytic.line']
            if task.project_id:
                project_aal = aal_obj.search([('project_id', '=', task.project_id.id)])
                total_wh += sum(aal.unit_amount for aal in project_aal)
            task.total_work_hour = total_wh

    @api.depends('total_sale_hour', 'total_work_hour')
    def _compute_available_hour(self):
        for task in self:
            task.available_hour = task.total_sale_hour - task.total_work_hour

    total_sale_hour = fields.Float(string='Horas vendidas', compute='_compute_total_sale_hour')
    total_work_hour = fields.Float(string='Horas trabajadas', compute='_compute_total_work_hour')
    available_hour = fields.Float(string='Horas disponibles del proyecto', compute='_compute_available_hour')
    department_id = fields.Many2one('hr.department', 'Departamento', store=True, related='project_id.department_id')

    def _find_mail_template(self):
        template_id = False
        template_id = int(self.env['ir.config_parameter'].sudo().get_param('processcontrol_sale_order.task_template'))
        template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
        if not template_id:
            raise UserError('No se encontro plantilla para mail de tareas')
        return template_id

    def action_task_report_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'project.task',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


class Project(models.Model):
    _inherit = 'project.project'

    @api.model
    def _cron_get_project_hours(self):
        for project in self.search([]):
            total_sh = 0
            total_wh = 0
            sol_obj = self.env['sale.order.line']
            project_sol = sol_obj.search([('project_id', '=', project.id)])
            for sol in project_sol:
                if sol.product_uom:
                    if 'hora' in sol.product_uom.name:
                        try:
                            total_sh += float(sol.product_uom.name.rsplit(' hora')[0].replace(',', '.')) * sol.qty_invoiced
                        except Exception as e:
                            continue
                    else:
                        total_sh += sol.qty_invoiced
            project.total_sale_hour = total_sh
            aal_obj = self.env['account.analytic.line']
            project_aal = aal_obj.search([('project_id', '=', project.id)])
            for aal in project_aal:
                total_wh += aal.unit_amount
            project.total_work_hour = total_wh
            project.available_hour = project.total_sale_hour - project.total_work_hour

    def compute_sales_hours(self):
        self.ensure_one()
        self.sales_hours = sum(self.task_ids.mapped('sales_hours'))

    total_sale_hour = fields.Float(string='Horas vendidas')
    total_work_hour = fields.Float(string='Horas trabajadas')
    available_hour = fields.Float(string='Horas disponibles')

    sales_hours = fields.Float(
        'Sale hours',
        compute='compute_sales_hours'
    )

    department_id = fields.Many2one('hr.department', 'Departamento')

    @api.onchange('user_id')
    def _onchange_user_id(self):
        for rec in self:
            if rec.user_id and rec.user_id.employee_id:
                rec.department_id = rec.user_id.employee_id.department_id.id
