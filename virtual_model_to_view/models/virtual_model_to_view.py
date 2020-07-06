# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, tools
import base64
import csv
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class VirtualModelToView(models.Model):
    _name = "virtual.model.to.view"
    _auto = "false"

    project_name = fields.Char(string='Nombre')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'project_milestone_invoicing')
        self._cr.execute("""
                CREATE OR REPLACE VIEW project_virtual AS (
                    SELECT 
                    ps.display_name as project_name
                    FROM public.project_project ps
                )""")