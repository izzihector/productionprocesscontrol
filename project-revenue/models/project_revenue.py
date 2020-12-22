# -*- coding: utf-8 -*-

from odoo import models, fields, api

class project_revenue(models.Model):
    _name = 'project_revenue.project_revenue'
    _description = 'project_revenue'
    _inherit = 'project.project'