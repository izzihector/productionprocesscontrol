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
    

