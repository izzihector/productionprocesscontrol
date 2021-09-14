# -*- encoding: utf-8 -*-
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_project(self):
        record = super(SaleOrderLine, self)._timesheet_create_project()
        if self.order_id.description:
            record.name = '%s - %s' % (self.order_id.name, self.order_id.description)

        return record
