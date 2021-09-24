# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SuscriptionLineSystemCenter(models.Model):
    _name = 'suscription.line.system.center'
    
    date=fields.Date(string='Fecha',readonly=True)
    partner_id = fields.Many2one(comodel_name='res.partner',string='Cliente SAGE',readonly=True)
    nro_sage = fields.Char(string='Nro SAGE',readonly=True)
    suscription_id = fields.Many2one(comodel_name='sale.subscription',string=u'Suscripción',readonly=True)
    suscription_line_id = fields.Many2one(comodel_name='sale.subscription.line',string='Linea de la suscripción',readonly=True)
    product_id = fields.Many2one(comodel_name='product.product',string='Producto',readonly=True)
    quantity= fields.Float(related='suscription_line_id.quantity',string='Cantidad actual', store=True,readonly=True)
    quantity_to_update = fields.Float(string='Cantidad en SC',readonly=True)
    state = fields.Selection([('draft','Pendiente'),('done','Validada')],string='Estado',default='draft')
    approved_by_id = fields.Many2one(comodel_name='res.users',string='Aprobado por',readonly=True)
    
    def action_update(self):
        lines = self.browse(self._context.get('active_ids', []))
        for line in lines:
            if line.state == 'done':
                raise ValidationError('Solamente se puede actualizar las lineas de las suscripciones que se encuentren en estado Pendiente')
        for line in lines:
            if line.suscription_line_id:
                line.suscription_line_id.quantity = line.quantity_to_update
                line.state = 'done'
                line.approved_by_id = self._uid
        
                
            





