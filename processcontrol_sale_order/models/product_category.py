# -*- coding: utf-8 -*-

from odoo import models, _, api
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    # Only user with the security group group_create_category or group_restrict_category_creation can change activities
    # The group_restrict_category_creation user can only change the categories selected in his Many2Many

    @api.model
    def create(self, values):
        if not self:
            if not self.env.user.has_group('processcontrol_sale_order.group_restrict_category_creation'):
                raise ValidationError(_('Error. No tienes el permiso para realizar esta acción'))
            available_categories = self.env['res.groups'].search(
                [('name', '=', 'Restringuir creación categoria de productos')], limit=1)
            if not self.env.user.has_group('processcontrol_sale_order.group_create_category'):
                category_available = False
                parent = self.browse(values.get('parent_id'))
                while not category_available and parent:
                    if parent in available_categories.category_ids:
                        category_available = True
                    parent = parent.parent_id
                if not category_available:
                    raise ValidationError(_('Error. No tienes el permiso para realizar esta acción'))
        return super(ProductCategory, self).create(values)

    def write(self, values):
        if not self.env.user.has_group('processcontrol_sale_order.group_restrict_category_creation'):
            raise ValidationError(_('Error. No tienes el permiso para realizar esta acción'))
        available_categories = self.env['res.groups'].search([('name', '=', 'Restringuir creación categoria de productos')], limit=1)
        if not self.env.user.has_group('processcontrol_sale_order.group_create_category'):
            category_available = self in available_categories.category_ids
            parent = self.parent_id if self.parent_id else False
            new_parent = values.get('parent_id', False)
            parent_category = False
            new_parent_category = True
            if new_parent:
                new_parent = self.browse(values.get('parent_id'))
                new_parent_category = False
            while not category_available and (parent or new_parent):
                if parent:
                    if parent in available_categories.category_ids:
                        parent_category = True
                    parent = parent.parent_id if parent.parent_id else False
                if new_parent:
                    if new_parent in available_categories.category_ids:
                        new_parent_category = True
                    new_parent = new_parent.parent_id if new_parent.parent_id else False
                if new_parent_category and parent_category:
                    category_available = True
            if not category_available:
                raise ValidationError(_('Error. No tienes el permiso para realizar esta acción'))
        return super(ProductCategory, self).write(values)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if not self.env.user.has_group('processcontrol_sale_order.group_restrict_category_creation'):
            raise ValidationError(_('Error. No tienes el permiso para realizar esta acción'))
        available_categories = self.env['res.groups'].search(
            [('name', '=', 'Restringuir creación categoria de productos')], limit=1)
        if not self.env.user.has_group('processcontrol_sale_order.group_create_category'):
            category_available = self in available_categories.category_ids
            parent = self.parent_id if self.parent_id else False
            while not category_available and parent:
                if parent in available_categories.category_ids:
                    category_available = True
                parent = parent.parent_id if parent.parent_id else False
            if not category_available:
                raise ValidationError(_('Error. No tienes el permiso para realizar esta acción'))
        return super(ProductCategory, self).copy(default=default)

    def unlink(self):
        if not self.env.user.has_group('processcontrol_sale_order.group_restrict_category_creation'):
            raise ValidationError(_('Error. No tienes el permiso para realizar esta acción'))
        available_categories = self.env['res.groups'].search(
            [('name', '=', 'Restringuir creación categoria de productos')], limit=1)
        if not self.env.user.has_group('processcontrol_sale_order.group_create_category'):
            category_available = self in available_categories.category_ids
            parent = self.parent_id
            while not category_available and parent:
                if parent in available_categories.category_ids:
                    category_available = True
                parent = parent.parent_id
            if not category_available:
                raise ValidationError(_('Error. No tienes el permiso para realizar esta acción'))
        return super(ProductCategory, self).unlink()
