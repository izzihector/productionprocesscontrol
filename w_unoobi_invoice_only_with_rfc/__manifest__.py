# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | Invoice Only With RFC',

    'summary': """Validation for the creation of invoices""",

    'description': """
        Valid that invoices cannot be created to clients that do not have RFC and address
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Extra Tools',

    'version': '14.0.0',

    'depends': ['base', 'account'],

    'data': [
            #'views/prealerts_views.xml',
           ],

    # 'qweb': [
    #         'static/src/xml/*.xml'
    #     ],

    'installable': True,

    'active': False,

    'certificate': '',

    'application':False,
}

