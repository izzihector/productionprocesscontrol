# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _, SUPERUSER_ID
from odoo.http import request, content_disposition
import re
import werkzeug
import base64
from odoo.tools import pycompat
from odoo.tools import groupby as groupbyelem
from operator import itemgetter
from odoo.osv.expression import OR
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
import logging
_logger = logging.getLogger(__name__)


class PortalTicketsProcessHelpDesk(CustomerPortal):

    # @http.route()
    # def my_helpdesk_tickets(self, page=1, date_begin=None, date_end=None,
    #                         sortby=None, filterby='all', search=None, groupby='none',
    #                         search_in='content', **kw):
    #     response = super().my_helpdesk_tickets(
    #         page=page, date_begin=date_begin, date_end=date_end, sortby=sortby,
    #         filterby=filterby, search=search, groupby=groupby, search_in=search_in, **kw
    #     )
    #     response.qcontext.update(
    #         {
    #             'date_begin': date_begin,
    #             'date_end': date_end,
    #         }
    #     )
    #     return response

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

    @http.route("/submitted/ticket", type="http", auth="user", website=True)
    def portal_submit_ticket(self, **kw):
        team_id = False
        if not kw.get("departament_id"):
            raise Warning ('Error no se pudo crear el ticket')
        elif kw.get("departament_id") == 'sistemas':
            team_id = request.env['helpdesk.team'].search([('name', '=', 'Soporte Sistemas Nivel 1')])
        else:
            team_id = request.env['helpdesk.team'].search([('name', '=', 'Soporte Software Nivel 1')])

        vals = {
            "name": kw.get("name"),
            "team_id": team_id.id if team_id else '',
            "partner_id": http.request.env.user.partner_id.id,
            "partner_email": http.request.env.user.email,
            "description": kw.get("description"),
        }

        new_ticket = request.env["helpdesk.ticket"].sudo().create(vals)

        if kw.get('attachment', False):
            attached_files = request.httprequest.files.getlist('attachment')
            for attachment in attached_files:
                attached_file = attachment.read()

                request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'res_model': 'helpdesk.ticket',
                    'res_id': new_ticket.id,
                    'type': 'binary',
                    'datas': pycompat.to_text(base64.b64encode(attached_file))
                })

        return werkzeug.utils.redirect("/my/ticket/" + str(new_ticket.id) + "?")

    @http.route(['/new/ticket'], type='http', auth="user", website=True)
    def portal_new_ticket(self):

        user = request.env.user
        values = {
            "u_name": user.name,
            "u_id": user.id,
            "u_mail": user.login,
        }

        return request.render("u_custom_process.portal_create_ticket_processcontrol", values)

    # @http.route(['/my/tickets', '/my/tickets/page/<int:page>'], type='http', auth="user", website=True)
    # def my_helpdesk_tickets(self, page=1, date_begin=None, date_end=None, sortby=None, filterby='all', search=None,
    #                         groupby='none', search_in='content', **kw):
    #     values = self._prepare_portal_layout_values()
    #
    #     searchbar_sortings = {
    #         'date': {'label': _('Newest'), 'order': 'create_date desc'},
    #         'name': {'label': _('Subject'), 'order': 'name'},
    #         'stage': {'label': _('Stage'), 'order': 'stage_id'},
    #         'reference': {'label': _('Reference'), 'order': 'id'},
    #         'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
    #     }
    #     searchbar_filters = {
    #         'all': {'label': _('All'), 'domain': []},
    #         'assigned': {'label': _('Assigned'), 'domain': [('user_id', '!=', False)]},
    #         'unassigned': {'label': _('Unassigned'), 'domain': [('user_id', '=', False)]},
    #         'open': {'label': _('Open'), 'domain': [('close_date', '=', False)]},
    #         'closed': {'label': _('Closed'), 'domain': [('close_date', '!=', False)]},
    #         'last_message_sup': {'label': _('Last message is from support')},
    #         'last_message_cust': {'label': _('Last message is from customer')},
    #     }
    #     searchbar_inputs = {
    #         'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
    #         'message': {'input': 'message', 'label': _('Search in Messages')},
    #         'customer': {'input': 'customer', 'label': _('Search in Customer')},
    #         'id': {'input': 'id', 'label': _('Search in Reference')},
    #         'status': {'input': 'status', 'label': _('Search in Stage')},
    #         'all': {'input': 'all', 'label': _('Search in All')},
    #     }
    #     searchbar_groupby = {
    #         'none': {'input': 'none', 'label': _('None')},
    #         'stage': {'input': 'stage_id', 'label': _('Stage')},
    #     }
    #
    #     # default sort by value
    #     if not sortby:
    #         sortby = 'date'
    #     order = searchbar_sortings[sortby]['order']
    #
    #     if filterby in ['last_message_sup', 'last_message_cust']:
    #         discussion_subtype_id = request.env.ref('mail.mt_comment').id
    #         messages = request.env['mail.message'].search_read(
    #             [('model', '=', 'helpdesk.ticket'), ('subtype_id', '=', discussion_subtype_id)],
    #             fields=['res_id', 'author_id'], order='date desc')
    #         last_author_dict = {}
    #         for message in messages:
    #             if message['res_id'] not in last_author_dict:
    #                 last_author_dict[message['res_id']] = message['author_id'][0]
    #
    #         ticket_author_list = request.env['helpdesk.ticket'].search_read(fields=['id', 'partner_id'])
    #         ticket_author_dict = dict(
    #             [(ticket_author['id'], ticket_author['partner_id'][0] if ticket_author['partner_id'] else False) for
    #              ticket_author in ticket_author_list])
    #
    #         last_message_cust = []
    #         last_message_sup = []
    #         for ticket_id in last_author_dict.keys():
    #             if last_author_dict[ticket_id] == ticket_author_dict[ticket_id]:
    #                 last_message_cust.append(ticket_id)
    #             else:
    #                 last_message_sup.append(ticket_id)
    #
    #         if filterby == 'last_message_cust':
    #             domain = [('id', 'in', last_message_cust)]
    #         else:
    #             domain = [('id', 'in', last_message_sup)]
    #
    #     else:
    #         domain = searchbar_filters[filterby]['domain']
    #
    #     if date_begin and date_end:
    #         domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
    #
    #     if request.env.user.partner_id:
    #         domain += [('partner_id', '=', request.env.user.partner_id.id)]
    #
    #     # search
    #     if search and search_in:
    #         search_domain = []
    #         if search_in in ('id', 'all'):
    #             search_domain = OR([search_domain, [('id', 'ilike', search)]])
    #         if search_in in ('content', 'all'):
    #             search_domain = OR(
    #                 [search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
    #         if search_in in ('customer', 'all'):
    #             search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
    #         if search_in in ('message', 'all'):
    #             discussion_subtype_id = request.env.ref('mail.mt_comment').id
    #             search_domain = OR([search_domain, [('message_ids.body', 'ilike', search),
    #                                                 ('message_ids.subtype_id', '=', discussion_subtype_id)]])
    #         if search_in in ('status', 'all'):
    #             search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
    #         domain += search_domain
    #
    #     # pager
    #     tickets_count = len(request.env['helpdesk.ticket'].search(domain))
    #     _logger.info('------------------------------------------------------------------------------------------------------------------------------------------')
    #     _logger.info(tickets_count)
    #     _logger.info('------------------------------------------------------------------------------------------------------------------------------------------')
    #     pager = portal_pager(
    #         url="/my/tickets",
    #         url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'search_in': search_in,
    #                   'search': search},
    #         total=tickets_count,
    #         page=page,
    #         step=self._items_per_page
    #     )
    #
    #     tickets = request.env['helpdesk.ticket'].search(domain, order=order, limit=self._items_per_page,
    #                                                     offset=pager['offset'])
    #     request.session['my_tickets_history'] = tickets.ids[:100]
    #
    #     if groupby == 'stage':
    #         grouped_tickets = [request.env['helpdesk.ticket'].concat(*g) for k, g in
    #                            groupbyelem(tickets, itemgetter('stage_id'))]
    #     else:
    #         grouped_tickets = [tickets]
    #
    #     values.update({
    #         'date': date_begin,
    #         'grouped_tickets': grouped_tickets,
    #         'page_name': 'ticket',
    #         'default_url': '/my/tickets',
    #         'pager': pager,
    #         'searchbar_sortings': searchbar_sortings,
    #         'searchbar_filters': searchbar_filters,
    #         'searchbar_inputs': searchbar_inputs,
    #         'searchbar_groupby': searchbar_groupby,
    #         'sortby': sortby,
    #         'groupby': groupby,
    #         'search_in': search_in,
    #         'search': search,
    #         'filterby': filterby,
    #     })
    #     return request.render("helpdesk.portal_helpdesk_ticket", values)
    #
    #     # @http.route(['/my/tickets/print_all_page'], type='http', auth="public", website=True)
    #     # def portal_my_tickets_all(self, all_tickets=False, **kw):
    #     #     report_type = 'pdf'
    #     #     report_ref = 'u_ticket_report.action_report_ticket'
    #     #     report_sudo = request.env.ref(report_ref).with_user(SUPERUSER_ID)
    #     #     # tickets_sudo = request.env['helpdesk.ticket'].with_user(SUPERUSER_ID).search([])
    #
    #     #     method_name = '_render_qweb_%s' % ('pdf')
    #     #     report = getattr(report_sudo, method_name)(eval(all_tickets), data={'report_type': 'pdf'})[0]
    #     #     reporthttpheaders = [
    #     #         ('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
    #     #         ('Content-Length', len(report)),
    #     #     ]
    #     #     filename = "%s.pdf" % (re.sub('\W+', '-', 'Informe de Tickets'))
    #     #     reporthttpheaders.append(('Content-Disposition', content_disposition(filename)))
    #     #     return request.make_response(report, headers=reporthttpheaders)
