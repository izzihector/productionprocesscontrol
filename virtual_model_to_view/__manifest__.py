# -*- coding: utf-8 -*-
{
    'name': "Creador de vistas SQL",

    'summary': """""",

    'description': """
        Monta una vista sql como modelo tipo Vista en Odoo
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        # 'security/groups.xml',
        #'data/data.xml',
        #'wizard/project_hour_revenue_summary_wizard.xml',
        #'report/project_hour_revenue_summary.xml',
        'views/views.xml',
    ],
    'installable': True,
    'auto_install': True,
    # only loaded in demonstration mode
    #'demo': [
        #'demo/demo.xml',
    #],
}