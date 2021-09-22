from odoo import models, fields, _, api
from odoo.exceptions import UserError


class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'
    _order = 'sequence'

    sequence = fields.Integer(string='Sequence', default=1)
    product_service_tracking = fields.Selection(related='product_id.service_tracking')
    cost = fields.Float('Cost')
    order_line_id = fields.Many2one('sale.order.line', 'Order line')
    project_id = fields.Many2one('project.project', 'Project')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")
    ], default=False, help="Technical field for UX purpose.")
    product_id = fields.Many2one(required=False)
    uom_id = fields.Many2one(required=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('display_type', self.default_get(['display_type'])['display_type']):
                vals.update(product_id=False, price_unit=0, quantity=0,
                            uom_id=False)
        return super(SaleSubscriptionLine, self).create(vals_list)

    def write(self, values):
        if 'display_type' in values and self.filtered(
                lambda line: line.display_type != values.get('display_type')):
            raise UserError(_(
                "You cannot change the type of an sale order line. Instead you "
                "should delete the current line and create a new line of "
                "the proper type."))
        return super(SaleSubscriptionLine, self).write(values)
