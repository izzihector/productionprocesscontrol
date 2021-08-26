# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | Sale Description Timesheet',

    'summary': """A description is added to the sales order which will be added in the creation of the project""",

    'description': """
        A description is added to the sales order which will be added in the creation of the project
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Sale',

    'version': '14.0.0',

    'depends': ['base', 'sale'],

    'data': [
            'views/inherit_sale_order_views.xml',
           ],

    # 'qweb': [
    #         'static/src/xml/*.xml'
    #     ],

    'installable': True,

    'active': False,

    'certificate': '',

    'application':False,
}

