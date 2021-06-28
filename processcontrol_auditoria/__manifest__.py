# -*- coding: utf-8 -*-
{
    'name': "Auditoria",

    'summary': """""",

    'description': """
       1. Crear nuevo módulo processcontrol_auditoria 
       2. Listado de precio de coste en 0
       3. Sin pedido de venta
    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_subscription', 'sale'],

    # always loaded
    'data': [
        'security/servicio_security.xml',
        'security/ir.model.access.csv',
        'views/audit_menu.xml',
        'views/sale_order_subscription_report_views.xml',
        'views/sale_order_cost_in_zero_views.xml',
        'views/project_without_sale_order_item_view.xml',
        'views/descargar_hojas_view.xml',
    ]
    # only loaded in demonstration mode
    # 'demo': [
    # 'demo/demo.xml',
    # ],
}
