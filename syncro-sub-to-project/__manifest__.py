# -*- coding: utf-8 -*-
{
    'name': "Syncro Subscription to project",

    'summary': """""",

    'description': """
        Conecta los proyectos con las lineas de suscripcion y con las facturas para poder obtener análisis
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Uncategorized',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['sale_subscription','base','project'], 

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'data/data.xml',
        #'wizard/project_hour_revenue_summary_wizard.xml',
        #'report/project_hour_revenue_summary.xml',
        # 'views/views.xml',
    ],
    'installable': True,
    'auto_install': True,
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],
}