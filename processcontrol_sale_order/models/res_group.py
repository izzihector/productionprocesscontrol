# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class res_groups_mail_channel(models.Model):
    _inherit = 'res.groups'

    def _compute_exclude_category(self):
        for res_gr in self:
            res_gr.exclude_category = res_gr.name == 'Restringuir creación categoria de productos'

    exclude_category = fields.Boolean(compute='_compute_exclude_category')
    category_ids = fields.Many2many('product.category', string='Categorias')



