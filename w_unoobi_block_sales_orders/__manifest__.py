# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | Block Sales Orders (Sale)',

    'summary': """Only users who belong to the unlock sell orders group will be able to unblock sales orders""",

    'description': """
        Only users who belong to the unlock sell orders group will be able to unblock sales orders
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Sale',

    'version': '14.0.0',

    'depends': ['base', 'sale'],

    'data': [
            'views/inherit_sale_order_views.xml',
            'security/security.xml',
           ],

    # 'qweb': [
    #         'static/src/xml/*.xml'
    #     ],

    'installable': True,

    'active': False,

    'certificate': '',

    'application':False,
}

