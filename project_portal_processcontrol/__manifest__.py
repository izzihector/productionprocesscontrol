# Copyright 2020 Raul Carbonell - raul.carbonell@processcontrol.es
# License AGPL-3.0 or later
{
    "name": "Project Portal Process Control",
    "summary":
         "Modificar Portal Proyecto/Tareas para Process Control",
    "version": "14.0.0",
    "category": "undefined",
    "website": "",
    "author": "Raul Carbonell",
    "license": "AGPL-3",
    "data": [
        "views/portal.xml",
        "views/project_portal_tasks.xml",
        "views/project_portal_projects.xml",
    ],
    "depends": [
        "base",
        "portal",
        "project"
    ],
    "application": False,
    "installable": True,
}
