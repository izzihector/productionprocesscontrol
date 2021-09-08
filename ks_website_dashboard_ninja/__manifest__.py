# -*- coding: utf-8 -*-
{
    'name': "Website Dashboard Ninja",

    'summary': """
        Revamp your Odoo Dashboard like never before! It is one of the best dashboard odoo apps in the market.
        """,

    'description': """
        V12 Dashboard
        Dashboard v12.0,
        Odoo Dashboard v12.0,
        Website Dashboard v12.0,
        Odoo Website Dashboards,
        Best Website Dashboard Apps
        Best Dashboard Apps
        Best Odoo Apps
        Dashboard For Websites
        Odoo Dashboard apps,
        Best Odoo Dashboard Apps
        Dashboard apps,
        Dashboards for Websites
        HR Dashboard Apps,
        Sales Dashboard Apps,
        inventory Dashboard Apps,
        Lead Dashboards,
        Opportunity Dashboards,
        CRM Dashboards,
        Best POS Apps
        POS Dashboards,
        Connectors
        Web Dynamic Apps,
        Report Import/Export,
        Date Filter Apps
        Tile Dashboard Apps
        Dashboard Widgets,
        Dashboard Manager Apps,
        Debranding Apps
        Customize Dashboard Apps
        Graph Dashboard Apps,
        Charts Dashboard Apps
        Invoice Dashboard Apps
        Project management Apps
    """,

    'author': "Ksolves India Ltd.",
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 99.0,
    'website': "https://www.ksolves.com",
    'maintainer': 'Ksolves India Limited',
    'live_test_url': 'https://websitedn14.kappso.com/',
    'category': 'Tools',
    'version': '14.0.1.1.2',
    'support': 'sales@ksolves.com',
    'images': ['static/description/banners/ks_website_dashboard_ninja_v14.gif'],
    'depends': ['base', 'website', 'ks_dashboard_ninja'],

    'data': [
        'security/ir.model.access.csv',
        'views/ks_assets.xml',
        'views/ks_snippets.xml',
        'views/ks_dashboard_ninja.xml',
    ],
    'qweb': [
        'ks_website_dashboard_ninja/static/src/xml/ks_website_no_item_template.xml',
    ],
}
