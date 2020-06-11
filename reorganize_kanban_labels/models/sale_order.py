# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    def deleteDuplicate(self):
        PTP = self.env['project.task.type']
        PT = self.env['project.task']

        etiquetas = PTP.search([])

        if etiquetas:
            for etiqueta in etiquetas:
                etiqueta_id = etiqueta.id
                tareas = PT.search([('stage_id', '=', etiqueta_id)])
                has_tasks = self.env['project.task'].search_count([('stage_id', '=', etiqueta_id)])

                if has_tasks == 0:
                    etiqueta.unlink()
