# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
from odoo import api, models, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    description= fields.Char('Description', help='The description will be concatenated to create the project name')



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_project(self):
        record= super(SaleOrderLine, self)._timesheet_create_project()
        if self.order_id.description != False:
            record.name= self.order_id.name + ' : ' + self.order_id.description
        return record