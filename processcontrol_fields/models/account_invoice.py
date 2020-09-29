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

        origen = vals['origin']
        SO = self.env['sale.order']
        SOL = self.env['sale.order.line']
        es_servicio = 0
        mensaje = ""

        if origen:
            if origen != "":
                pedido = SO.search([('name', '=', origen)])
                if pedido:
                    pedido_id = pedido.id
                    lineas_pedido = SOL.search([('order_id', '=', pedido_id)])
                    if lineas_pedido:
                        for linea in lineas_pedido:
                            producto = linea.product_id
                            if producto:
                                categoria_es_servicio_proyecto_cerrado = producto.categ_id.category_for_project_closed
                                if categoria_es_servicio_proyecto_cerrado:
                                    es_servicio = 1
                                    if linea.x_studio_proyecto_pedido_venta.id == "" or linea.x_studio_proyecto_pedido_venta.id == False:
                                        # Si entra en esta condicion, no tiene proyecto indicado pero si que lo necesita
                                        mensaje = mensaje + "\n En la linea del producto: " + producto.name + " es obligado establecer un proyecto."
                                        if linea.product_uom_qty == 1:
                                            if linea.horas_reales == 0:
                                                mensaje = mensaje + "\n La linea del producto: " + producto.name + " no puede tener 0 horas reales."

                                    if linea.x_studio_proyecto_pedido_venta.id:
                                        if linea.product_uom_qty == 1:
                                            if linea.horas_reales == 0:
                                                mensaje = mensaje + "\n La linea del producto: " + producto.name + " no puede tener 0 horas reales."

        if es_servicio == 1 and mensaje != "":
            raise ValidationError(_(mensaje))

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