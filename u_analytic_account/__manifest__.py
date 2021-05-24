# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Analytic Account Management',
    'version': '14.0.0',
    'category': 'Sale',
    'description': """
Modifications to account analytic accounts in sales
========================================
    """,
    'depends': ['base', 'sale_subscription'],
    'author': 'Unoobi',
    'website': 'http://www.unoobi.com',
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_analytic_views.xml',
        'views/account_move_views.xml',
    ],
    'qweb': [],
    'application': False,
}
