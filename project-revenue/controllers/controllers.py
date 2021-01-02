# -*- coding: utf-8 -*-
from odoo import http

class ProjectRevenue(http.Controller):
    @http.route('/project_revenue/project_revenue/', auth='public')
    def index(self, **kw):
        return "Hello, world"