# -*- coding: utf-8 -*-
{
    'name': 'Unoobi | Custom Process',

    'summary': """Customization to Process""",

    'description': """
        Customization to Process
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Uncategorized',

    'version': '14.0.0',

    'depends': [
        'base',
        'sale_management',
        "sale_margin",
        "helpdesk",
        "u_ticket_report",
        "u_project_report",
        "project_portal_processcontrol"
    ],

    'data': [  
        # === SECURITY
        "security/ir.model.access.csv",
        # === VIEWS
        "views/helpdesk_views.xml", 
        'views/assets.xml',
        'views/sale_order.xml',
        # 'views/portal.xml',
        'views/helpdesk_portal_templates.xml',      
        'views/project_portal_tasks.xml',      
        'wizard/create_task_from_oportunity_view.xml',      
        'views/res_config_settings_views.xml',      
        'views/crm_lead_views.xml',      
    ],
}