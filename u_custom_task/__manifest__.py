# -*- encoding: utf-8 -*-
###############################################################################
#
#    Module Writen to Odoo12, Open Source Management Solution
#
############################################################################
{
    'name': 'Unoobi | Custom Task',

    'summary': """Assign tasks to parent tasks that belong to the selected project (Project)""",

    'description': """
        Assign tasks to parent tasks that belong to the selected project (Process) 
    """,

    'author': 'UNOOBI ©',

    "website" : "https://www.unoobi.com/",

    'category': 'Extra Tools',

    'version': '14.0.0.0',

    'depends': ['base', 'project'],

    'data': [
            'views/inherit_project_task_views.xml'
           ],

    # 'qweb': [
    #         'static/src/xml/*.xml'
    #     ],

    'installable': True,

    'active': False,

    'certificate': '',

    'application':False,
}

