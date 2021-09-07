# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from datetime import date, timedelta


class Project(models.Model):
    _inherit = "project.project"

    def write_mail_body_project_less_than_seven_days(self, project_without_assignment_less_than_seven_days_ids):
        message_body = u'Estimado, <br/> A continuación se presenta un listado de proyectos sin asignar creados hace 7 días: <br/>'
        message_body += '<br/>'
        for project in project_without_assignment_less_than_seven_days_ids:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            base_url += '/web?#id=%s&action=393&model=%s&view_type=form&menu_id=236' % (project.id, project._name)
            message_body += '   - Proyecto: <a href="%s">%s</a> del cliente %s. Creado el: %s' % (base_url,project.name, project.partner_id.name, project.create_date )
            message_body += '<br/>'
        return message_body

    def write_mail_body_project_more_than_seven_days(self, project_without_assignment_more_than_seven_days_ids):
        message_body = u'Estimado, <br/> A continuación se presenta un listado de proyectos sin asignar creados hace más de 7 días: <br/>'
        message_body += '<br/>'
        for project in project_without_assignment_more_than_seven_days_ids:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            base_url += '/web?#id=%s&action=393&model=%s&view_type=form&menu_id=236' % (project.id, project._name)
            message_body += '   - Proyecto: <a href="%s">%s</a> del cliente %s. Creado el: %s' % (base_url,project.name, project.partner_id.name, project.create_date)
            message_body += '<br/>'
        return message_body

    def cron_project_without_assignment(self):
        project_project_obj = self.env['project.project']
        less_seven_days = date.today() - timedelta(days=7)
        project_without_assignment_less_than_seven_days_ids = project_project_obj.search([('create_date', '>=', less_seven_days),('create_date','<=',date.today()),('user_id','=',False)])
        if project_without_assignment_less_than_seven_days_ids:
            project_without_assignment_more_than_seven_days_ids = project_project_obj.search([('id', 'not in', project_without_assignment_less_than_seven_days_ids.ids),('user_id','=',False)])
        else:
            project_without_assignment_more_than_seven_days_ids = project_project_obj.search([('user_id', '=', False)])

        if project_without_assignment_less_than_seven_days_ids:
            users_to_send = 'carolina.fernandez@processcontrol.es'
            message_body = self.write_mail_body_project_less_than_seven_days(project_without_assignment_less_than_seven_days_ids)
            odoobot = "envios@processcontrol.es"
            mail = self.env['mail.mail']
            mail_data = {'subject': u'Listado de proyectos sin asignar creados hace 7 días',
                         'email_from': odoobot,
                         'email_to': users_to_send,
                         'body_html': message_body,
                         }
            mail_out = mail.create(mail_data)
            mail_out.send()

        if project_without_assignment_more_than_seven_days_ids:
            users_to_send = 'carolina.fernandez@processcontrol.es'
            message_body = self.write_mail_body_project_more_than_seven_days(project_without_assignment_more_than_seven_days_ids)
            odoobot = "envios@processcontrol.es"
            mail = self.env['mail.mail']
            mail_data = {'subject': u'Listado de proyectos sin asignar creados hace más de 7 días',
                             'email_from': odoobot,
                             'email_to': users_to_send,
                             'body_html': message_body,
                             }
            mail_out = mail.create(mail_data)
            mail_out.send()
        return True