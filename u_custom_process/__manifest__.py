# -*- coding: utf-8 -*-
{
    'name': 'Unoobi | Custom Process',

    'summary': """Customization to Process""",

    'description': """
        Customization to Process
        1- Modificación Formulario Creación Tickets
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Uncategorized',

    'version': '14.0.0',

    'depends': [
        'base',
        'sale_management',
        'hr',
        "sale_margin",
        "helpdesk",
        'crm',
        'portal',
        'project',
        'processcontrol_sale_order',
        'website'


    ],

    'data': [  
        # === SECURITY
        "security/ir.model.access.csv",
        # === VIEWS
       # "views/helpdesk_views.xml",
        'views/assets.xml',
       # 'views/sale_order.xml',
        'views/hr_departament.xml',
        'views/portal.xml',
        'views/project_portal_new_ticket_template.xml',
        'views/helpdesk_portal_templates.xml',
        'views/project_portal_tasks.xml',      
        'wizard/create_task_from_oportunity_view.xml',      
        'views/res_config_settings_views.xml',      
        'views/crm_lead_views.xml',
       # 'views/project_views.xml',
    ],
}