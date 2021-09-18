{
    'name': 'Modificación de partes de horas',
    'summary': "Modificación de partes de horas.",
    'version': '1.0',
    'category': 'Hidden',
    'author': "ProcessControl",
    'website': "https://www.processcontrol.es",
    'description': """
Modificación de partes de horas.
================================
 - Añadir campo con estado indicando si la línea del parte de horas está dentro del teimpo planificado o lo supera.
 - Añadir ventana de chat para control de cambios.
 - Añadir vistas para controloar partes modificados.
 """,
    'depends': ['timesheet_grid', 'hr_timesheet', 'processcontrol_sale_order'],
    'installable': True,
    'auto_install': False,
    'data': [
        'views/project_task.xml',
        'views/account_analytic_line.xml'
    ]
}
