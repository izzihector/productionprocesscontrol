# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields
from datetime import date
from odoo.exceptions import UserError


class PCMandatosMasivos(models.TransientModel):
    _name = 'pc.automatizacion.sepa'

    def _get_need_partner(self):
        return not(dict(self._context or {}).get('active_ids', False))

    format = fields.Selection([
        ('basic', 'Mandato básico'),
        ('sepa', 'Mandato SEPA')
    ], string='Formato', required=True, default='sepa')

    type = fields.Selection([
        ('generic', 'Mandato Genérico'),
        ('recurrent', 'Recurrente'),
        ('oneoff', 'Único')
    ], string='Tipo', required=True, default='recurrent')

    recurrent_sequence_type = fields.Selection([
        ('first', 'Primero'),
        ('recurring', 'Recurrente'),
        ('final', 'Final')
    ], string='Tipo de Secuencia', default='first', help='Tipo de secuencia para el siguiente debito')

    scheme = fields.Selection([
        ('CORE', 'Básico (CORE)'),
        ('B2B', 'Empresa (B2B)')
    ], string='Esquema', required=True, default='CORE')
    signature_date = fields.Date(string="Fecha de la firma del mandato", required=True, default=date.today())
    need_partner = fields.Boolean(string='Necesita Contactos', default=_get_need_partner)
    partner_ids = fields.Many2many('res.partner', string='Clientes')

    def create_sepa(self):
        """
        This function create a mandate for all the partner selected
        if this partner has at least one bank account and there isn't
        one already created
        """
        context = dict(self._context or {})
        if context.get('active_ids', False):
            contacts = self.env['res.partner'].browse(context.get('active_ids'))
        elif self.partner_ids:
            contacts = self.partner_ids
        else:
            raise UserError('Debe seleccionar por lo menos un cliente')
        abm_obj = self.env['account.banking.mandate']
        new_abm_ids = abm_obj
        for contact in contacts:
            if not contact.bank_ids:
                raise UserError('El cliente %s no tiene cuentas bancarias asociadas' % contact.name)
            for bank in contact.bank_ids:
                if not abm_obj.search([('partner_id', '=', contact.id), ('partner_bank_id', '=', bank.id)]):
                    new_abm = abm_obj.create({
                        'format': self.format,
                        'type': self.type,
                        'recurrent_sequence_type': self.recurrent_sequence_type,
                        'scheme': self.scheme,
                        'signature_date': self.signature_date,
                        'partner_bank_id': bank.id,
                        'partner_id': contact.id
                    })
                    new_abm_ids += new_abm
        if new_abm_ids:
            return {
                'domain': [('id', 'in', new_abm_ids.ids)],
                'name': 'Banking Mandates',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.banking.mandate',
                'view_id': False,
                'views': [(self.env.ref('account_banking_mandate.view_mandate_tree').id, 'tree'),
                          (self.env.ref('account_banking_mandate.view_mandate_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }
        else:
            return {'type': 'ir.actions.act_window_close'}



