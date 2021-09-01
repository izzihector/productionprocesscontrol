# -*- coding: utf-8 -*-
{
    'name': "Alertas por Correo",

    'summary': """""",

    'description': """
        1-Enviar email tareas vencidos y por vencer
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['project'],

    # always loaded
    'data': [
        'data/data_cron.xml',
    ]
    # only loaded in demonstration mode
    # 'demo': [
    # 'demo/demo.xml',
    # ],
}
