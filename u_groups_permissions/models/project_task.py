# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def unlink(self):
        if self.env.user.has_group('u_groups_permissions.group_can_not_delete_task'):
            raise ValidationError(_('Error. You do not have permissions for delete tasks'))
        return super(ProjectTask, self).unlink()

    def write(self, vals):
        if 'active' in vals:
            if self.env.user.has_group('u_groups_permissions.group_can_not_archive_project_and_task'):
                raise ValidationError(_('Error. You do not have permissions for archive tasks'))
        return super(ProjectTask, self).write(vals)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def write(self, vals):
        if 'active' in vals:
            if self.env.user.has_group('u_groups_permissions.group_can_not_archive_project_and_task'):
                raise ValidationError(_('Error. You do not have permissions for archive projects'))
        return super(ProjectProject, self).write(vals)
