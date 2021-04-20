# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | RFC Duplication Control (Contacts)',

    'summary': """Prevent two contacts from registering with the same RFC""",

    'description': """
        Prevent two contacts from registering with the same RFC
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Contacts',

    'version': '14.0.0',

    'depends': ['base', 'contacts'],

    'data': [
            'views/inherit_res_partner_views.xml',
           ],

    # 'qweb': [
    #         'static/src/xml/*.xml'
    #     ],

    'installable': True,

    'active': False,

    'certificate': '',

    'application':False,
}

