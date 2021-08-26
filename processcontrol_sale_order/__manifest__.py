# -*- coding: utf-8 -*-
{
    'name': "Cambios en los pedidos de ventas y subscripciones",

    'summary': """""",

    'description': """
       1. Cuando se cambie la fecha de próxima factura en la suscripción que quede en la red social el detalle de los cambios 
       2. Quitar filtro en el campo Plantilla de proyecto en la vista formulario de product.product. y product.template
       3. Al crear la oportunidad, por defecto se debe crear con el comercial asociado al cliente y no con el usuario logueado en el sistema.
       4. Al cambiar el comercial en el cliente/proveedor se debe todos sus contactos hijos, en caso de que los tenga.
       5. Agregar nombre fantasía en la ficha de clientes
       6. Cambiar la búsqueda de proyectos para que salga primero cliente/contacto.
       7. Precio de coste sea modificable cuando el pedido de venta esta bloqueado/confirmado.
       8. Limitar la creación de proyectos.
       9. Agregar pestana etapas en los proyectos.
       10. Agregar en la impresión del pedido de venta los campos agregados en los productos opciones (Total, descuento en caso de que tenga, etc).
       11. Agregar botón para Enviar tarea por mail.
       12. Reporte de ventas quitar el label de la unidad de medida.
       13. Notificar a los usuarios el alta de una actividad en suscripcion.
       14. Imprimir suscripciones.   
       15. Solamente el grupo de seguridad unlock sale order puede desbloquear pedidos de ventas
       16. Reporte de tareas modificar
       17. Tareas: Agregar nuevo botón "Add description""
       18. En los presupuestos, que el presupuesto salga desde quien envía el presupuesto y no desde el comercial.
       19. Error al enviar presupuesto
       20. Generar informe de los pedidos de venta generados desde las suscripciones nueva hoja
       21. Error al crear una suscripcion
       22. PRECIO DE COSTE EN RED SOCIAL PRESUPUESTOS
       23. DUPLICAR PRESUPUESTO
       23. CREACIÓN DE FACTURA DESDE EL PEDIDO DE VENTA
       24. Modificar reporte de facturas
       25. Editar actividades de otros compañeros
       26. Pagos de Vencimiento en Facturas
       27. Tickets: Agregar nuevo botón "Add description"
       28. Nuevo grupo de seguridad: Eliminar parte de horas.
       29. Restringir en el alta de productos las familias a informar
       30. Quitar dominio en los diarios que figuran en los asientos contables
       31. Campo comercial en la ficha de contactos como requerido
       32. Importar Empleado Responsable
       33. Cuando se crea oportunidad, fecha de cierre a 6 meses
       34. El formato del reporte de la suscripcion debe ser igual al del pedido de venta
       35. Formato de impresión del pedido de compra tiene que ser el mismo que el pedido de venta

    """,

    'author': "ProcessControl",
    'website': "http://www.processcontrol.es",
    'category': 'Revenues',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['account', 'base', 'sale_subscription', 'crm', 'product', 'project', 'sale', 'u_project_report','w_unoobi_block_sales_orders', 'helpdesk', 'u_groups_permissions'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/product_view.xml',
        'views/menu_item_view.xml',
        'views/my_task_menu.xml',
        'views/crm_lead_view.xml',
        'views/res_partner_view.xml',
        'views/res_group_view.xml',
        'data/cron.xml',
        'data/mail_data.xml',
        'data/sale_data.xml',
        'data/task_data.xml',
        'report/project_task_add_description_view.xml',
        'report/inherit_external_layout_sale_order_views.xml',
        'report/sale_report.xml',
        'report/sale_report_templates.xml',
        'report/purchase_order_report_templates.xml',
        'report/helpdesk_ticket_add_description_view.xml',
        'report/sale_report_templates.xml',
        'wizard/process_import_empleado_responsable_view.xml',
        # 'report/account_report_invoice_templates.xml',
        'report/sale_subscription_report.xml',
        'report/sale_subscription_report_template.xml',
        'views/project_view.xml',
        'views/sale_subscription_view.xml',
        'views/sale_order_view.xml',
        'security/ir.model.access.csv',
        'report/sale_report_templates.xml',
        'views/account_move_view.xml',
    ]
    # only loaded in demonstration mode
    # 'demo': [
    # 'demo/demo.xml',
    # ],
}
