# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID

_logger = logging.getLogger(__name__)


class Lead(models.Model):
    _inherit = "crm.lead"
    _description = "Lead/Opportunity"

    
    date_deadline = fields.Date(tracking=True, default=lambda self: date.today() + relativedelta(months=+3))
    task_count = fields.Integer('# Task', compute='_compute_task_count')
    task_tech_count = fields.Integer('# Task', compute='_compute_task_tech_count')
    timesheet_ids_count = fields.Integer('# Task', compute='_compute_timesheet_count')
    timesheet_encode_uom_id = fields.Many2one('uom.uom', related='company_id.timesheet_encode_uom_id')
    tech_timesheet_ids_count = fields.Integer('# Task', compute='_compute_tech_timesheet_count')

    def _compute_task_count(self):
        if self.ids:
            task_data = self.env['project.task'].sudo().read_group([
                ('opportunity_id', 'in', self.ids),('process_type', '=', 'normal')
            ], ['opportunity_id'], ['opportunity_id'])
            mapped_data = {m['opportunity_id'][0]: m['opportunity_id_count'] for m in task_data}
        else:
            mapped_data = dict()
        for lead in self:
            lead.task_count = mapped_data.get(lead.id, 0)
    
    def _compute_task_tech_count(self):
        if self.ids:
            task_data = self.env['project.task'].sudo().read_group([
                ('opportunity_id', 'in', self.ids),('process_type', '=', 'tech')
            ], ['opportunity_id'], ['opportunity_id'])
            mapped_data = {m['opportunity_id'][0]: m['opportunity_id_count'] for m in task_data}
        else:
            mapped_data = dict()
        for lead in self:
            lead.task_tech_count = mapped_data.get(lead.id, 0)
    
    def _compute_timesheet_count(self):        
        for lead in self:
            task_ids = self.env['project.task'].sudo().search([
                ('opportunity_id', '=', lead.id),('process_type', '=', 'normal')
            ])
            total_time = 0.0
            for timesheet in task_ids.timesheet_ids:
                # Timesheets may be stored in a different unit of measure, so first
                # we convert all of them to the reference unit
                total_time += timesheet.unit_amount * timesheet.product_uom_id.factor_inv
            # Now convert to the proper unit of measure set in the settings
            total_time *= task_ids.project_id.timesheet_encode_uom_id.factor
            lead.timesheet_ids_count = int(round(total_time))
    
    def _compute_tech_timesheet_count(self):        
        for lead in self:
            task_ids = self.env['project.task'].sudo().search([
                ('opportunity_id', '=', lead.id),('process_type', '=', 'tech')
            ])
            total_time = 0.0
            for timesheet in task_ids.timesheet_ids:
                # Timesheets may be stored in a different unit of measure, so first
                # we convert all of them to the reference unit
                total_time += timesheet.unit_amount * timesheet.product_uom_id.factor_inv
            # Now convert to the proper unit of measure set in the settings
            total_time *= task_ids.project_id.timesheet_encode_uom_id.factor
            lead.tech_timesheet_ids_count = int(round(total_time))

    def action_view_tasks(self):
        """ Open task's on current opportunity.
            :return dict: dictionary value for created Task view
        """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("project.action_view_all_task")
        action['domain'] = [('opportunity_id', '=', self.id),('process_type', '=', 'normal')]
        return action
    
    def action_view_tasks_tech(self):
        """ Open task's on current opportunity.
            :return dict: dictionary value for created Task view
        """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("project.action_view_all_task")
        action['domain'] = [('opportunity_id', '=', self.id),('process_type', '=', 'tech')]
        return action
    
    def action_view_tasks_timesheet(self):
        """ Open task's timesheet on current opportunity.
            :return dict: dictionary value for created Task Timesheet view
        """
        self.ensure_one()
        task_ids = self.env['project.task'].sudo().search([
            ('opportunity_id', 'in', self.ids)
        ])
        action = self.env["ir.actions.actions"]._for_xml_id("hr_timesheet.timesheet_action_task")
        action['domain'] = [('task_id', 'in', task_ids.ids)]
        return action
    
    def action_view_tasks_timesheet_tech(self):
        """ Open task's timesheet on current opportunity.
            :return dict: dictionary value for created Task Timesheet view
        """
        self.ensure_one()
        task_ids = self.env['project.task'].sudo().search([
            ('opportunity_id', 'in', self.ids), ('process_type', '=', 'tech')
        ])
        action = self.env["ir.actions.actions"]._for_xml_id("hr_timesheet.timesheet_action_task")
        action['domain'] = [('task_id', 'in', task_ids.ids)]
        return action
    

