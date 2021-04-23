# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _, SUPERUSER_ID
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError, UserError
from collections import OrderedDict
from odoo.http import request, content_disposition
import re
import werkzeug


class PortalTicketsProcessHelpDesk(CustomerPortal):   

    @http.route()
    def my_helpdesk_tickets(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None, groupby='none', search_in='content', **kw):
    
        response = super().my_helpdesk_tickets(
            page=page, date_begin=date_begin, date_end=date_end, sortby=sortby, filterby=filterby, search=search, groupby=groupby, search_in=search_in, **kw
        )
        response.qcontext.update(
            {
                'date_begin': date_begin,
                'date_end': date_end,
            }
        )
        return response        
 

    @http.route(['/my/tickets/print_current_page'], type='http', auth="public", website=True)
    def portal_my_tickets_current(self, tickets=False, **kw):
        if eval(tickets):
            report_type = 'pdf'
            report_ref = 'u_ticket_report.action_report_ticket'
            report_sudo = request.env.ref(report_ref).with_user(SUPERUSER_ID)
            # tickets_sudo = request.env['helpdesk.ticket'].with_user(SUPERUSER_ID).search([])

            method_name = '_render_qweb_%s' % ('pdf')
            report = getattr(report_sudo, method_name)(eval(tickets), data={'report_type': 'pdf'})[0]
            reporthttpheaders = [
                ('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
                ('Content-Length', len(report)),
            ]
            filename = "%s.pdf" % (re.sub('\W+', '-', 'Informe de Tickets'))
            reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
            return request.make_response(report, headers=reporthttpheaders)

    @http.route(['/my/tasks/print_current_page'], type='http', auth="public", website=True)
    def portal_my_tasks_current(self, tasks=False, **kw):
        if eval(tasks):
            report_type = 'pdf'
            report_ref = 'u_project_report.action_report_services_part'
            report_sudo = request.env.ref(report_ref).with_user(SUPERUSER_ID)

            method_name = '_render_qweb_%s' % ('pdf')
            report = getattr(report_sudo, method_name)(eval(tasks), data={'report_type': 'pdf'})[0]
            reporthttpheaders = [
                ('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
                ('Content-Length', len(report)),
            ]
            filename = "%s.pdf" % (re.sub('\W+', '-', 'Informe de Tickets'))
            reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
            return request.make_response(report, headers=reporthttpheaders)
        else:
            return werkzeug.utils.redirect("my/tickets")

    # @http.route(['/my/tickets/print_all_page'], type='http', auth="public", website=True)
    # def portal_my_tickets_all(self, all_tickets=False, **kw):
    #     report_type = 'pdf'
    #     report_ref = 'u_ticket_report.action_report_ticket'
    #     report_sudo = request.env.ref(report_ref).with_user(SUPERUSER_ID)
    #     # tickets_sudo = request.env['helpdesk.ticket'].with_user(SUPERUSER_ID).search([])

    #     method_name = '_render_qweb_%s' % ('pdf')
    #     report = getattr(report_sudo, method_name)(eval(all_tickets), data={'report_type': 'pdf'})[0]
    #     reporthttpheaders = [
    #         ('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
    #         ('Content-Length', len(report)),
    #     ]
    #     filename = "%s.pdf" % (re.sub('\W+', '-', 'Informe de Tickets'))
    #     reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
    #     return request.make_response(report, headers=reporthttpheaders)
