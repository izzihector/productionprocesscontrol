# -*- coding: utf-8 -*-
{
    'name': "Análisis Económico de proyectos",

    'summary': """""",

    'description': """
        Genra un informe de horas vendidas vs horas imputadas en los proyectos seleccionados
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','project','sale_management','timesheet_grid','sale_subscription'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'data/data.xml',
       # 'wizard/project_hour_revenue_summary_wizard.xml',
        #'report/project_hour_revenue_summary.xml',
        'views/views.xml',
    ]
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],
}