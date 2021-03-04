# -*- coding: utf-8 -*-
{
    'name': "u_project_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Report Service part of tasks by projects.
    """,

    'author': "Unoobi",
    'website': "http://www.unoobi.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_pdf_services_part.xml',
        'report/report_pdf_services_part_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}