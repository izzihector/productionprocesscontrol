# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Uom system archive restriction',
    'version': '14.0.0',
    'category': 'Sale',
    'description': """
Do not allow regular users to archive an unarchive uom
========================================
    """,
    'depends': ['base', 'sale_subscription'],
    'author': 'Unoobi',
    'website': 'http://www.unoobi.com',
    'data': [
        # Security
        'security/groups.xml'
    ],
    'qweb': [],
    'application': False,
}
