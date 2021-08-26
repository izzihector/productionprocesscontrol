# -*- coding: utf-8 -*-
{
    'name': "Conctact Create Lead",

    'summary': """""",

    'description': """
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/create_lead_view.xml',
    ]
    # only loaded in demonstration mode
    # 'demo': [
    # 'demo/demo.xml',
    # ],
}
