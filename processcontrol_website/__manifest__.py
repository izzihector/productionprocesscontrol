# -*- coding: utf-8 -*-
{
    'name': "Website - Process Control",

    'summary': """""",

    'description': """
       1. Al crear una tarea en la web, me tiene que redireccionar a una pagina que diga tarea nueva tarea creada
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Website',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['website', 'portal'],

    # always loaded
    'data': [
           'views/my_account_template.xml',
    ]
    # only loaded in demonstration mode
    # 'demo': [
    # 'demo/demo.xml',
    # ],
}
