# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields
from xlrd import open_workbook
from odoo.exceptions import ValidationError, UserError
import io
import base64
import datetime


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
        updated=str()
        self.dont_found = False
        if not self.archive:
            sale_subscription_lines = self.env['sale.subscription.line'].search([('product_id.product_tmpl_id','in',(1481,1603,1482,299)),('cost','<=',0)])
            for line in sale_subscription_lines:
                line.cost = 0.01
                count_so += 1
            if count_so >0:
                self.updated = 'Se actualizaron %s lineas de suscripciones' % count_so + '\n'

            # sale_orders = self.env['sale.order'].search([('user_id','!=',False)])
            # teams= self.env['crm.team'].search([])
            # agosto = datetime.datetime(2021, 9, 1)
            # for sale in sale_orders:
            #     if sale.user_id not in sale.team_id.member_ids:
            #         for team in teams:
            #             if sale.user_id in team.member_ids:
            #                 if (sale.user_id.id == 407 and sale.date_order < agosto) or sale.user_id.id != 407:
            #                     sale.team_id = team.id
            #                     count_so+=1
            # if count_so >0:
            #     updated += 'Se actualizaron %s pedidos de venta' % count_so + '\n'
            # count_so = float()
            # opportunities = self.env['crm.lead'].search([('type','=','opportunity'),('user_id', '!=', False)])
            # for oportunity in opportunities:
            #     if oportunity.user_id not in oportunity.team_id.member_ids:
            #         for team in teams:
            #             if oportunity.user_id in team.member_ids:
            #                 if (oportunity.user_id.id == 407 and oportunity.create_date < agosto) or oportunity.user_id.id != 407:
            #                     oportunity.team_id = team.id
            #                     count_so+=1
            # if count_so >0:
            #     updated += 'Se actualizaron %s oportunidades' % count_so + '\n'
            # suscriptions = self.env['sale.subscription'].search([('user_id', '!=', False)])
            # count_so = float()
            # for suscription in suscriptions:
            #     if suscription.user_id not in suscription.team_id.member_ids:
            #         for team in teams:
            #             if suscription.user_id in team.member_ids:
            #                 if (suscription.user_id.id == 407 and suscription.create_date < agosto) or suscription.user_id.id != 407:
            #                         suscription.team_id = team.id
            #                         count_so+=1
            # if count_so >0:
            #     updated += 'Se actualizaron %s suscripciones' % count_so + '\n'

            if updated:
                self.updated = updated





