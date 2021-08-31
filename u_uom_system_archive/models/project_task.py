# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import ValidationError


# class ProjectTask(models.Model):
#     _inherit = 'project.task'
#
#     def write(self, vals):
#         if 'active' in vals:
#             if not self.env.user.has_group('u_uom_system_archive.group_can_archive_tasks'):
#                 raise ValidationError(_('Error. Only a user with permision Can archive tasks'
#                                         ' can perform this action'))
#         return super(ProjectTask, self).write(vals)
