# -*- coding: utf-8 -*-
{
    'name': "Campos añadidos para el funcionamiento correcto de ProcessControl",

    'summary': """""",

    'description': """
        Genera campos necesarios para el correcto funcionamiento de ProcessControl
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','account','sale_subscription','helpdesk', 'project', 'crm'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/views.xml',
    ]
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],
}
