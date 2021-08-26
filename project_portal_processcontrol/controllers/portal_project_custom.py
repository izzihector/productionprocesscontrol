
import werkzeug

from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
import base64
from odoo.tools import pycompat

from odoo.osv.expression import OR


class CustomerPortalProcess(CustomerPortal):

    @http.route("/submitted/task", type="http", auth="user", website=True)
    def portal_submit_task(self,  **kw):
        if kw.get("parent_id")=="0":
            parentid=False
        else:
            task=request.env["project.task"].sudo().browse(int(kw.get("parent_id")))
            parentid=task.id

        project=request.env["project.project"].sudo().browse(int(kw.get("project_id")))

        vals = {
            "name": kw.get("name"),
            "company_id": http.request.env.user.company_id.id,
            "parent_id": parentid,
            "project_id": project.id,
            "partner_id": http.request.env.user.partner_id.id,
            "description": kw.get("description"),
        }

        new_task = request.env["project.task"].sudo().create(vals)

        if kw.get('attachment', False):
            attached_files = request.httprequest.files.getlist('attachment')
            for attachment in attached_files:
                attached_file = attachment.read()

                request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'res_model': 'project.task',
                    'res_id': new_task.id,
                    'type': 'binary',
                    'datas': pycompat.to_text(base64.b64encode(attached_file))
                })

        return werkzeug.utils.redirect("/my/task/" + str(new_task.id) + "?")

    @http.route(['/new/task'], type='http', auth="user", website=True)
    def portal_new_task(self, filterby=None, **kw):
        values={
        }
        if not filterby or filterby=='all':
            return werkzeug.utils.redirect("/my/tasks")
            #===================================================================
            # return request.render("project.portal_my_tasks", values)
            #===================================================================

        project=request.env['project.project'].search([('id','=', int(filterby))])

        tareas_padre_filters = {
            '0': {'label': _('Ninguno')},

        }

        tareaspadre=request.env['project.task'].search([('project_id','=', int(filterby)),('parent_id','=',False)], order='name asc')
        for task in tareaspadre:
            tareas_padre_filters.update({
                str(task.id): {'label': task.name}
            })


        values={
            "filterby": filterby,
            "project_name":project.name,
            "project_id":project.id,
            'tareas_padre_filters': OrderedDict(tareas_padre_filters.items()),
        }

        return request.render("project_portal_processcontrol.portal_create_task_processcontrol", values)

    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tasks(self, page=1, date_begin=None, date_end=None, sortby=None, stageby=None, filterby=None, search=None, search_in='content', groupby='project', **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'parent_id:' : {'label': _('Tarea Padre'), 'order': 'parent_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }

        #crear valores del filtro para stage
        stage_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'stage': {'input': 'stage', 'label': _('Search in Stages')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'project': {'input': 'project', 'label': _('Project')},
            'parent_id': {'input': 'parent_id', 'label': _('Tarea Padre')},
        }



        # extends filterby criteria with project the customer has access to
        projects = request.env['project.project'].search([])
        for project in projects:
            searchbar_filters.update({
                str(project.id): {'label': project.name, 'domain': [('project_id', '=', project.id)]}
            })

        # añadir las etapas de las tareas
        if not filterby or filterby=='all':
            tasks = request.env['project.task'].search([])
        else:
            tasks = request.env['project.task'].search([('project_id','=', int(filterby))])
        #tasks = request.env['project.task'].search([searchbar_filters[filterby]['domain']])
        for task in tasks:
            stage_filters.update({
                str(task.stage_id.id): {'label': task.stage_id.name, 'domain': [('stage_id', '=', task.stage_id.id)]}
            })

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env['project.task'].read_group([('project_id', 'not in', projects.ids)],
                                                                ['project_id'], ['project_id'])
        for group in project_groups:
            proj_id = group['project_id'][0] if group['project_id'] else False
            proj_name = group['project_id'][1] if group['project_id'] else _('Others')
            searchbar_filters.update({
                str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
            })



        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

         # valor por defecto en stagebym y meter valor el dominio para filtrar
        if not stageby:
            stageby = 'all'
        domain += stage_filters[stageby]['domain']

        # archive groups - Default Group By 'create_date'
        # archive_groups = self._get_archive_groups('project.task', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
            if search_in in ('stage', 'all'):
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain += search_domain

        # task count
        task_count = request.env['project.task'].search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/tasks",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'stageby': stageby, 'filterby': filterby, 'search_in': search_in, 'search': search, 'groupby': groupby },
            total=task_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        if groupby == 'project':
            order = "project_id, %s" % order  # force sort on project first to group by project in view
        tasks = request.env['project.task'].search(domain, order=order, limit=self._items_per_page, offset=(page - 1) * self._items_per_page)
        request.session['my_tasks_history'] = tasks.ids[:100]
        if groupby == 'project':
            grouped_tasks = [request.env['project.task'].concat(*g) for k, g in groupbyelem(tasks, itemgetter('project_id'))]
        elif groupby == 'parent_id':
            grouped_tasks = [request.env['project.task'].concat(*g) for k, g in groupbyelem(tasks, itemgetter('parent_id'))]
        else:
            grouped_tasks = [tasks]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': grouped_tasks,
            'page_name': 'task',
            # 'archive_groups': archive_groups,
            'default_url': '/my/tasks',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'stage_filters': OrderedDict(sorted(stage_filters.items())),
            'filterby': filterby,
            'stageby': stageby,
        })
        return request.render("project.portal_my_tasks", values)
