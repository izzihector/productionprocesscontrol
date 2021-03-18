# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def compute_sales_hours(self):
        self.ensure_one()
        self.sales_hours = sum(self.task_ids.mapped('sales_hours'))

    sales_hours = fields.Float(
        'Sale hours',
        compute='compute_sales_hours'
    )

    department_id = fields.Many2one('hr.department', 'Department')

class ProjectTask(models.Model):
    _inherit = 'project.task'

    #@api.multi
    def write(self, vals):
        for task in self:
            if vals.get('planned_hours', False) and not self.sales_hours:
                task.sales_hours = vals['planned_hours']
        return super(ProjectTask, self).write(vals)
    
    @api.model
    def create(self, vals_list):
        res = super(ProjectTask, self).create(vals_list)
        res.sales_hours = res.planned_hours
        self._create_line_subscription(res)
        return res

    #@api.multi
    def unlink(self):
        for task in self:
            if task.sales_hours != 0:
                raise ValidationError(_("Task cannot be deleted!"))
        return super(ProjectTask, self).unlink()

    sales_hours = fields.Float(
        'Sale hours'
    )

    product_subscription = fields.One2many('product.subscription', 'task_id', string='Product subscription')
    product_subscription_total = fields.Float(compute='_compute_product_subscription_total', string="Total", store=True)

    @api.depends('product_subscription', 'product_subscription.quantity', 'product_subscription.price_subtotal')
    def _compute_product_subscription_total(self):
        for aux in self:
            aux.product_subscription_total = sum(line.price_subtotal for line in aux.product_subscription)
        return

    def _create_line_subscription(self, record):
        list_subscription= self.env['sale.subscription'].search([('partner_id', '=', record.partner_id.id)])
        line_subscription= list_subscription.mapped('recurring_invoice_line_ids')
        filter_line= line_subscription.filtered(lambda line: line.product_id.show_product == True)

        line_vals = []
        for line in filter_line:
            params = {
                'product_id': line.product_id.id,
                'sale_subscription_line_id': line.id,
            }
            line_vals.append((0, 0, params))
        record.update({
            'product_subscription': line_vals
        })
        return