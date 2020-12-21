# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Subscriptions management',
    'version': '1.0',
    'category': 'Sale',
    'description': """
Modifications to subscriptions
========================================
    """,
    'depends': ['base', 'sale_subscription', 'project', 'timesheet_grid'],
    'author': 'Unoobi',
    'website': 'http://www.unoobi.com',
    'data': [
        'security/ir.model.access.csv',
        'views/sale_subscription_view.xml',
        'views/sale_order.xml',
    ],
    'qweb': [],
    'application': False,
}
