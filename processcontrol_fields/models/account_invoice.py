# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = ['account.invoice']

    numero_factura_sage = fields.Char(
        string='Numero Factura Sage',
        required=False)

    @api.model
    def create(self, vals):
        str = "SUB"
        origen = vals['origin']
        isProyectoCerrado = 0
        if(origen):
            if (str not in origen):
                SO = self.env['sale.order']
                orden = SO.search([('name','=', origen)])
                if(orden):
                    for dataOrder in orden:
                        idOrden = dataOrder.id
                        SOL = self.env['sale.order.line']
                        lineasPedido = SOL.search([('order_id','=', idOrden)])
                        if(lineasPedido):
                            for dataLineaPedido in lineasPedido:
                                lineaParaProyectoCerrado = dataLineaPedido.x_studio_proyecto_cerrado
                                lineaProyecto = dataLineaPedido.x_studio_proyecto_pedido_venta
                                if(lineaParaProyectoCerrado == True):
                                    if(lineaProyecto.id == False):
                                        raise exceptions.UserError(_("No puedes facturar este pedido. Contiene lineas de proyecto cerrado y no esta informado el mismo") % ())

        invoice = super(AccountInvoice, self).create(vals)
        payterm = False

        if (str in invoice.origin):
            SSL = self.env['sale.subscription']
            suscripciones = SSL.search([('name', '=', invoice.origin)])

            if (suscripciones):
                for sub in suscripciones:
                    payterm = sub.termino_pago
                    idSubscription = sub.id
                    nombreSuscripcion = sub.name

                    invoice.write({'payment_term_id': payterm.id})

        return invoice