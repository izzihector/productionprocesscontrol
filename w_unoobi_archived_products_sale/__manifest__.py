# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | Archived Product (Sale)',

    'summary': """Don't advance sales documents with archived products""",

    'description': """
        Prevent a quote from being passed to a sales order, or a sales order from creating an invoice 
        if it contains a product in its lines that is archived
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Sale',

    'version': '14.0.0',

    'depends': ['base', 'sale'],

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

