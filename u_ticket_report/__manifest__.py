# -*- coding: utf-8 -*-
{
    'name': "u_ticket_report",

    'summary': """
        The purpose of this module is to create a report of the service parts of the tickets.""",

    'description': """
        Ticket report in helpdesk.
    """,

    'author': "Unoobi",
    'website': "http://www.unoobi.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'helpdesk', 'helpdesk_timesheet'],

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