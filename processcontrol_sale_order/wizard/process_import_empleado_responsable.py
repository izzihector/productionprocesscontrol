# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields
from xlrd import open_workbook
from odoo.exceptions import ValidationError, UserError
import io
import base64


class PCImportEmpleadoResponsable(models.TransientModel):
    _name = 'pc.import.empleado.responsable'
    _description = 'pc.import.empleado.responsable'

    dont_found = fields.Text(string='No encontrados')
    updated = fields.Text(string="Actualizados")
    archive = fields.Binary(string="Archivo", attachment=True)

    def import_empledo_responsable(self):
        """
        This function recieve and excel with 2 column : SaleOrderName / Empleado Responsable
        and search the sale.order by name and if it found one update the field empleado_responable_id
        else add the SaleOrderName in dont_found
        """
        """
        This function recieve and excel with 2 column : SaleOrderName / Empleado Responsable
        and search the sale.order by name and if it found one update the field empleado_responable_id
        else add the SaleOrderName in dont_found
        """
        count_so=float()
        self.dont_found = False
        if not self.archive:
            sale_orders = self.env['sale.order'].search([('sale_order_type_id','=',1),('sub_template_id','=',False)])
            for sale in sale_orders:
                suscription = self.env['sale.subscription'].search([('code','=',sale.origin)],limit=1)
                if suscription:
                    sale.sub_template_id=suscription.template_id.id
                    count_so += 1
            if count_so:
                self.updated = 'Se actualizaron %s pedidos de venta' % count_so



