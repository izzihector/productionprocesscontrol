# -*- coding: utf-8 -*-
{
    'name': "Reorganizar etapas kanbans duplicadas",

    'summary': """""",

    'description': """
        Reorganiza las etapas que han sido duplicadas en los Kanban
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','account'],

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