# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields
from xlrd import open_workbook
from odoo.exceptions import ValidationError, UserError
import io
import base64


class PCImportEmpleadoResponsable(models.TransientModel):
    _name = 'pc.import.empleado.responsable'

    dont_found = fields.Text(string='No encontrados')
    updated = fields.Text(string="Actualizados")
    archive = fields.Binary(string="Archivo", attachment=True, required=True)

    def import_empledo_responsable(self):
        """
        This function recieve and excel with 2 column : SaleOrderName / Empleado Responsable
        and search the sale.order by name and if it found one update the field empleado_responable_id
        else add the SaleOrderName in dont_found
        """
        self.dont_found = False
        if not self.archive:
            raise UserError('Debe subir su archivo primero')
        with io.BytesIO(base64.b64decode(self.archive)) as f:
            try:
                book = open_workbook(file_contents=f.getvalue())
            except TypeError as e:
                raise ValidationError(u'ERROR: {}'.format(e))
            sheet = book.sheets()[0]
            count_so = 0
            sale_order_obj = self.env['sale.order']
            users_obj = self.env['res.users']
            for row in range(sheet.nrows):
                if row == 0:
                    if sheet.cell_value(row, 0) != 'Nombre':
                        raise UserError('Se espera columna "Nombre" en A1')
                    if sheet.cell_value(row, 1) != 'Empleado':
                        raise UserError('Se espera columna "Empleado" en B1')
                else:
                    if not sheet.cell_value(row, 0):
                        if self.dont_found:
                            self.dont_found += '\n' + ('No se encontro pedido de venta en la fila %s' % str(row+1))
                        else:
                            self.dont_found = 'No se encontro pedido de venta en la fila %s' % str(row+1)
                        continue
                    so = sale_order_obj.search([('name', '=', sheet.cell_value(row, 0))])
                    if not so:
                        if self.dont_found:
                            self.dont_found += '\n' + ('El pedido de venta %s no se encontro' % sheet.cell_value(row, 0))
                        else:
                            self.dont_found = 'El pedido de venta %s no se encontro' % sheet.cell_value(row, 0)
                        continue
                    if len(so) > 1:
                        if self.dont_found:
                            self.dont_found += '\n' + ('El pedido de venta %s se encontro mas de una vez' % sheet.cell_value(row, 0))
                        else:
                            self.dont_found = 'El pedido de venta %s se encontro mas de una vez' % sheet.cell_value(row, 0)
                        continue
                    if not sheet.cell_value(row, 1):
                        if self.dont_found:
                            self.dont_found += '\n' + ('No se encontro empleado en la fila %s' % str(row+1))
                        else:
                            self.dont_found = 'No se encontro empleado en la fila %s' % str(row+1)
                        continue
                    empleado_responsable = users_obj.search([('name', '=', sheet.cell_value(row, 1))])
                    if not empleado_responsable:
                        if self.dont_found:
                            self.dont_found += '\n' + ('El usuario %s no se encontro' % sheet.cell_value(row, 1))
                        else:
                            self.dont_found = 'El usuario %s no se encontro' % sheet.cell_value(row, 1)
                        continue
                    if len(empleado_responsable) > 1:
                        if self.dont_found:
                            self.dont_found += '\n' + ('El usuario %s se encontro mas de una vez' % sheet.cell_value(row, 1))
                        else:
                            self.dont_found = 'El usuario %s se encontro mas de una vez' % sheet.cell_value(row, 1)
                        continue
                    so.empleado_responsable_id = empleado_responsable.id
                    count_so += 1
            if count_so:
                self.updated = 'Se actualizaron %s pedidos de venta' % count_so
