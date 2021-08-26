# -*- coding: utf-8 -*-
{
    'name': "Expense Type",

    'summary': """""",

    'description': """
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['hr_expense', 'hr', 'base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/sage_report_view.xml',
        'views/pc_expense_type_view.xml',
        'views/pc_plus_productividad_view.xml',
        'views/hr_expense_view.xml',
        'views/hr_employee_view.xml',
    ]
    # only loaded in demonstration mode
    # 'demo': [
    # 'demo/demo.xml',
    # ],
}
