# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | Notify Subscriptions',

    'summary': """Notify a user by creating an automatic activity when registering a subscription.""",

    'description': """
        Notify a user by creating an automatic activity when registering a subscription, 
        the user to be notified must be registered in the subscription template.
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Sale',

    'version': '14.0.0',

    'depends': ['base', 'sale_subscription'],

    'data': [
            'views/inherit_sale_subscription_template_views.xml',
           ],

    # 'qweb': [
    #         'static/src/xml/*.xml'
    #     ],

    'installable': True,

    'active': False,

    'certificate': '',

    'application':False,
}

