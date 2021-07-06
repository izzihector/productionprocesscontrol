# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class descargar_hojas(models.TransientModel):
    _name = 'descargar.hojas'
    _description = 'Modelo para descargar archivos'

    archivo_nombre = fields.Char(string='Nombre del archivo')
    archivo_contenido = fields.Binary(string="Archivo")
