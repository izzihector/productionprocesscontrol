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
            sale_orders = self.env['sale.order'].search([('user_id','!=',False)])
            teams= self.env['crm.team'].search([]) 
            for sale in sale_orders:
                if sale.user_id not in sale.team_id.member_ids:
                    for team in teams:
                        if sale.user_id in team.member_ids:
                            if (sale.user_id.id == 407 and sale.create_date <= '2021-08-31') or sale.user_id.id != 407:
                                sale.team_id = team.id
                                count_so+=1
            self.updated += 'Se actualizaron %s pedidos de venta' % count_so + '\n'
            count_so = float()
            opportunities = self.env['crm.lead'].search([('type','=','opportunity'),('user_id', '!=', False)])
            for oportunity in opportunities:
                if oportunity.user_id not in oportunity.team_id.member_ids:
                    for team in teams:
                        if oportunity.user_id in team.member_ids:
                            if (oportunity.user_id.id == 407 and oportunity.create_date <= '2021-08-31') or oportunity.user_id.id != 407:
                                oportunity.team_id = team.id
                                count_so+=1
            self.updated += 'Se actualizaron %s oportunidades' % count_so + '\n'
            suscriptions = self.env['sale.subscription'].search([('user_id', '!=', False)])
            count_so = float()
            for suscription in suscriptions:
                if suscription.user_id not in suscription.team_id.member_ids:
                    for team in teams:
                        if suscription.user_id in team.member_ids:
                            if (suscription.user_id.id == 407 and suscription.create_date <= '2021-08-31') or suscription.user_id.id != 407:
                                    suscription.team_id = team.id
                                    count_so+=1
            self.updated += 'Se actualizaron %s suscripciones' % count_so + '\n'

            #     suscription = self.env['sale.subscription'].search([('code','=',sale.origin)],limit=1)
            #     if suscription:
            #         sale.sub_template_id=suscription.template_id.id
            #         count_so += 1
            # if count_so:
            #     self.updated = 'Se actualizaron %s pedidos de venta' % count_so



