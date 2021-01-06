# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | Sale Report (Process)',

    'summary': """The layout of the sales report is custom (Process).""",

    'description': """
        The layout of the sales report is custom (Process).
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Sale',

    'version': '1.0',

    'depends': ['base', 'sale'],

    'data': [
            'report/inherit_sale_report_templates.xml',
           ],

    # 'qweb': [
    #         'static/src/xml/*.xml'
    #     ],

    'installable': True,

    'active': False,

    'certificate': '',

    'application':False,
}

