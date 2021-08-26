# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('sale_order_option_ids.price_subtotal')
    def _amount_all_option(self):
        for order in self:
            amount = 0.0
            for option in order.sale_order_option_ids:
                amount += option.price_subtotal
            order.update({
                'amount_total_option': amount,
            })

    @api.depends('order_line')
    def _compute_total_purchase_price(self):
        for subscription in self:
            subscription.total_purchase_price = sum(x.purchase_price for x in self.order_line)

    total_purchase_price = fields.Float(string='Total Purchase Price', compute='_compute_total_purchase_price',
                                        track_visibility='always')
    margin = fields.Monetary("Margin", compute='_compute_margin', store=True, track_visibility='always')
    amount_total_option = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all_option', tracking=4)
    empleado_responsable_id = fields.Many2one(comodel_name='res.users',string='Empleado responsable',track_visibility='always')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if self.subscription_count:
            raise UserError(_("Can't duplicate a sale order that is linked to a subscription"))
        copied_sale_order_id = super(SaleOrder, self).copy(default=default)
        return copied_sale_order_id

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = False

        if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('processcontrol_sale_order.default_confirmation_template'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('processcontrol_sale_order.mail_template_sale_confirmation',
                                                                        raise_if_not_found=False)
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('processcontrol_sale_order.email_template_edi_sale',
                                                                    raise_if_not_found=False)

        return template_id

    def action_quotation_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        uid = self.env['res.users'].browse(self._context['uid'])
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'uid_mail': uid.email_formatted,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_cancel(self):
        """ If an order line have a project, check if any of the tasks of that project have a timesheet
            if that so we raise an UserError else we archive the project """
        for order in self:
            for line in order.order_line:
                if line.project_id:
                    for task in line.project_id.task_ids:
                        if task.timesheet_ids:
                            raise UserError('No se puede cancelar un pedido que tiene parte de horas asignado.')
                    line.project_id.active = False
        return super(SaleOrder, self).action_cancel()

    def action_confirm(self):
        """ If the product of an order line is not active we raise an User Error"""
        for order in self:
            for line in order.order_line:
                if line.product_id and not line.product_id.active:
                    raise UserError('No se puede confirmar el presupuesto porque el producto %s se encuentra archivado.' % line.product_id.name)
        return super(SaleOrder, self).action_confirm()


class SaleOrderOption(models.Model):
    _inherit = "sale.order.option"

    @api.depends('quantity', 'discount', 'price_unit') # , 'tax_id' ver si es necesario agregar campo impuesto
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * line.quantity * (1 - (line.discount or 0.0) / 100.0)
            line.update({
                'price_subtotal': price,
            })

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    currency_id = fields.Many2one(related='order_id.currency_id', depends=['order_id.currency_id'], store=True,
                                  string='Currency', readonly=True)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"

    def create_invoices(self):
        """ If the product of an order line in a sale order is not active we raise an User Error"""
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for order in sale_orders:
            for line in order.order_line:
                if line.product_id and not line.product_id.active:
                    raise UserError(
                        'No se puede crear la factura porque el producto %s del pedido de venta %s se encuentra archivado.' % (line.product_id.name, order.name))
        return super().create_invoices()

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super()._prepare_invoice_values(order, name, amount, so_line)
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_task(self, project):
        """Generate an activity if the new project has a task named 'Planificar proyecto'"""
        a_planificar = self.env['project.task'].search([('name', '=', 'Planificar proyecto'), ('project_id', '=', project.id)], limit=1)
        if a_planificar:
            to_do_activity = self.env['mail.activity.type'].search([('name', '=', 'To Do')], limit=1).id
            res_model_id = self.env['ir.model'].sudo().search([('model', '=', a_planificar._name)], limit=1).id
            mail_activity_obj = self.env['mail.activity']
            note = '<p>Asignar técnico si ya esta definido. Poner info adicional para proyecto</p>'
            if not mail_activity_obj.search([('res_model', '=', a_planificar._name), ('res_id', '=', a_planificar.id),
                                             ('note', '=', note)]):
                mail_activity_obj.create({
                    'res_model_id': res_model_id,
                    'res_model': a_planificar._name,
                    'res_id': a_planificar.id,
                    'res_name': a_planificar.name,
                    'activity_type_id': to_do_activity,
                    'note': note,
                    'date_deadline': date.today(),
                    'user_id': self.order_id.user_id.id,
                })
        return super(SaleOrderLine, self)._timesheet_create_task(project)
