# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from datetime import date


class Task(models.Model):
    _inherit = "project.task"

    def write_mail_body(self, employee, expiration_tasks):
        message_body = 'Estimado/a %s, <br/> A continuacion se presenta un listado de tareas vencidas y/o que vencen el día de hoy: <br/>' % employee
        message_body += '<br/>'
        for task in expiration_tasks:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            base_url += '/web?#id=%s&action=1162&model=%s&view_type=form&menu_id=236' % (task.id, task._name)
            exp_date = 'vence hoy' if task.date_deadline == date.today() else (u'venció el día <b> %s </b>' % task.date_deadline.strftime("%d/%m/%Y"))
            message_body += '   - La tarea <a href="%s">%s</a> del cliente %s %s ' % (base_url,task.name, task.partner_id.name, exp_date)
            message_body += '<br/>'
        return message_body

    def cron_tasks_expiration(self):
        project_taks_obj = self.env['project.task']
        end_stage = self.env['project.task.type'].search([('name', 'in', ('Finalizado', 'Finalizada'))])
        tasks_expired = project_taks_obj.search([('date_deadline', '<=', date.today()), ('stage_id', 'not in', end_stage.ids), ('user_id', '=', 538)])
        dic_employee = {}
        for task in tasks_expired:
            if task.user_id in dic_employee:
                dic_employee[task.user_id].append(task)
            else:
                dic_employee = {task.user_id: [task]}
        for employee in dic_employee:
            users_to_send = employee.login
            message_body = self.write_mail_body(employee.name, dic_employee[employee])
            odoobot = "envios@processcontrol.es"
            mail = self.env['mail.mail']
            mail_data = {'subject': 'Tareas vencidas o que vencen el dia de hoy',
                         'email_from': odoobot,
                         'email_to': users_to_send,
                         'body_html': message_body,
                         }
            mail_out = mail.create(mail_data)
            mail_out.send()
            return True



