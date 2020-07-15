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
    _auto = False

    id = fields.Integer (string="Identificador")
    project_name = fields.Char(string='Nombre')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self._cr.execute("""CREATE OR REPLACE VIEW %s AS 
          (SELECT row_number() OVER () as id, ps.name as project_name FROM public.project_project ps LIMIT 10)"""% self._table)