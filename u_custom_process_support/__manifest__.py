# -*- coding: utf-8 -*-
{
    'name': 'Unoobi | Process Support Post-Sale',

    'summary': """Process Support Post-Sale""",

    'description': """
        Process Support Post-Sale
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Helpdesks',

    'version': '14.0.0',

    'depends': [
        "base",        
        "helpdesk",        
    ],

    'data': [  
        # === SECURITY
        "security/ir.model.access.csv",
        # === DATAS
        "data/mail_template_data.xml", 
        # === VIEWS
        "views/inherit_res_partner.xml",    
        "views/product_type_views.xml",    
    ],
}