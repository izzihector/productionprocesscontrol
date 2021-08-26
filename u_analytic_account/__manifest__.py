# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Analytic Account Management',
    'version': '1.0',
    'category': 'Sale',
    'description': """
Modifications to account analytic accounts in sales
========================================
    """,
    'depends': ['base', 'analytic', 'sale'],
    'author': 'Unoobi',
    'website': 'http://www.unoobi.com',
    'data': [
        #'security/ir.model.access.csv',
        'views/account_analytic_views.xml',
    ],
    'qweb': [],
    'application': False,
}
