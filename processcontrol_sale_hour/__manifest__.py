# -*- coding: utf-8 -*-
{
    'name': "Project Total Hours",

    'summary': """""",

    'description': """
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'sale'],

    # always loaded
    'data': [
        'views/project_view.xml',
    ]
    # only loaded in demonstration mode
    # 'demo': [
    # 'demo/demo.xml',
    # ],
}
