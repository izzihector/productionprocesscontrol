# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
import base64
import csv
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class VirtualModelToView(models.Model):
    _name = "virtual_model_to_view"

    name = fields.Char(string='Nombre')