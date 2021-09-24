# -*- coding: utf-8 -*-
{
    'name': "System Center Integración - Process Control",

    'summary': """""",

    'description': """

    """,

    'author': "ProcessControl",
    'website': "https://www.processcontrol.es",
    'category': 'Website',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_subscription'],

    # always loaded
    'data': [
        'views/configuration_view.xml',
        'views/subscription_system_center_view.xml',
        'views/menu_view.xml',
        'security/ir.model.access.csv'
        
        
    ]
    # only loaded in demonstration mode
    # 'demo': [
    # 'demo/demo.xml',
    # ],
}
