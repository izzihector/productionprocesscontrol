# -*- coding: utf-8 -*-
{
    'name': "Visualizador DML",

    'summary': """""",

    'description': """
        
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'data/data.xml',
        #'wizard/project_hour_revenue_summary_wizard.xml',
        #'report/project_hour_revenue_summary.xml',
        'views/views.xml',
    ],
    'installable': True,
    'auto_install': False,
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],
}