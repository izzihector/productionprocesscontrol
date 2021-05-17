# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | Invoice Report (Process)',

    'summary': """The design of the invoice report is customized (Process).""",

    'description': """
        The design of the invoice report is customized (Process). 
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Extra Tools',

    'version': '14.0.0.1',

    'depends': ['base', 'account'],

    'data': [
            'views/inherit_report_invoice.xml',
            'views/inherit_external_layout_views.xml',
            'views/layouts.xml',
           ],

    # 'qweb': [
    #         'static/src/xml/*.xml'
    #     ],

    'installable': True,

    'active': False,

    'certificate': '',

    'application':False,
}

