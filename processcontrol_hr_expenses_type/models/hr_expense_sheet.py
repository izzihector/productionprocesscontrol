

from odoo import fields, models, _, api
from odoo.exceptions import UserError
from datetime import date
import pdb


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    date_approval = fields.Date(string=u'Fecha de aprobación', track_visibility='onchange', readonly=True)
    payment_date = fields.Date(string='Fecha de pago', track_visibility='onchange', readonly=True)

    def write(self, values):
        if 'state' in values:
            if values['state'] == 'done':
                values['payment_date']=date.today()
            if values['state'] == 'approve':
                values['date_approval']=date.today()
        return super(HrExpenseSheet, self).write(values)
