# -*- encoding: utf-8 -*-
{
    'name': 'Unoobi | Sale Description Timesheet',
    'summary': """A description is added to the sales order which will be added in the creation of the project""",
    'description': """
        A description is added to the sales order which will be added in the creation of the project
    """,
    'author': 'UNOOBI ©',
    "website": "https://www.unoobi.com/",
    'category': 'Sale',
    'version': '14.0.0',
    'depends': ['base', 'sale', 'sale_project'],
    'data': [
        'views/inherit_sale_order_views.xml',
    ],

    'installable': True,
    'active': False,
    'certificate': '',
    'application': False,
}
