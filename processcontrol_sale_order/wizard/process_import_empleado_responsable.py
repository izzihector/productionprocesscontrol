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
            project_task_obj = self.env['project.task']
            for row in range(sheet.nrows):
                if row == 0:
                    if sheet.cell_value(row, 0) != 'ID':
                        raise UserError('Se espera columna "Nombre" en A1')
                    if sheet.cell_value(row, 1) != 'Resolucion':
                        raise UserError('Se espera columna "Empleado" en B1')
                else:
                    if not sheet.cell_value(row, 0):
                        if self.dont_found:
                            self.dont_found += '\n' + ('No se encontro el ID en la fila %s' % str(row+1))
                        else:
                            self.dont_found = ' No se encontro el ID en la fila %s' % str(row+1)
                        continue
                    task_id = project_task_obj.search([('id', '=', sheet.cell_value(row, 0))])
                    if not task_id:
                        if self.dont_found:
                            self.dont_found += '\n' + ('No se encontro la tarea con ID %s' % sheet.cell_value(row, 0))
                        else:
                            self.dont_found = 'No se encontro la tarea con ID %s' % sheet.cell_value(row, 0)
                        continue
                    if len(task_id) > 1:
                        if self.dont_found:
                            self.dont_found += '\n' + ('Tarea con ID %s se encontro mas de una vez' % sheet.cell_value(row, 0))
                        else:
                            self.dont_found = 'Tarea con ID %s se encontro mas de una vez' % sheet.cell_value(row, 0)
                        continue
                    task_id.x_resolucion = sheet.cell_value(row, 1)
                    count_so += 1
            if count_so:
                self.updated = 'Se actualizaron %s tareas' % count_so


