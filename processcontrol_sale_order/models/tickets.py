# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.model
    def create(self, vals):
        """
        It is inherited to prepare the message in the creation of the ticket.

        @param vals:
        """
        res = super(HelpdeskTicket, self).create(vals)
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
                            content += "  \u2022 Duración: " + '{0:02.0f}:{1:02.0f}'.format(
                                *divmod(new_val * 60, 60)) + "<br/>"
                        elif change_vals == 'name' and new_val:
                            content += "  \u2022 Descripción: " + new_val + "<br/>"
                elif ts[0] == 2:
                    if content != "Parte de Horas: <br/>":
                        content += "------------------------------------------------------------------------------<br/>"
                    unlinked_aal = aal_obj.browse(ts[1])
                    content += "  \u2022 Elimino la parte de hora %s de %s horas<br/>" % \
                               (unlinked_aal.name,
                                '{0:02.0f}:{1:02.0f}'.format(*divmod(unlinked_aal.unit_amount * 60, 60)))
                elif ts[0] == 1:
                    if content != "Parte de Horas: <br/>":
                        content += "------------------------------------------------------------------------------<br/>"
                    aal_changed = aal_obj.browse(ts[1])
                    for change_vals in ts[2]:
                        new_val = ts[2][change_vals]
                        if change_vals == 'date':
                            content += "  \u2022 Fecha: " + aal_changed.date.strftime(
                                "%d/%m/%Y") + "&#8594;" + new_val + "<br/>"
                        elif change_vals == 'employee_id':
                            new_employee = self.env['hr.employee'].browse(new_val).name
                            content += "  \u2022 Empleado: " + aal_changed.employee_id.name + "&#8594;" + new_employee + "<br/>"
                        elif change_vals == 'name':
                            content += "  \u2022 Descripción: " + aal_changed.name + "&#8594;" + (
                                new_val if new_val else ' ') + "<br/>"
                        elif change_vals == 'unit_amount':
                            content += "  \u2022 Descripción: " + '{0:02.0f}:{1:02.0f}'.format(
                                *divmod(aal_changed.unit_amount * 60, 60)) \
                                       + "&#8594;" + '{0:02.0f}:{1:02.0f}'.format(*divmod(new_val * 60, 60)) + "<br/>"

        if content == "Parte de Horas: <br/>":
            content = ''
        self.message_post(body=content)
        return super(HelpdeskTicket, self).write(values)
