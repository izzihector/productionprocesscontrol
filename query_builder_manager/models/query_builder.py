# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class QueryBuilder(models.Model):
    _name = 'query.builder'
    # _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Query Builder Manager DML'

    query = fields.Text(
        string='Query',
        required=False)

    name = fields.Char(
        string='Title',
        required=False)

    @api.multi
    def get_result(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'query': self.query,
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('query_builder.query_summary').report_action(
            self, data=data)

class QueryBuilderReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.query_builder.query_builder_report_view'

    @api.multi
    def _get_report_values(self, docids, data=None):
        query = self.query
        docs = []

        docs['query'] = query

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }

