# -*- coding: utf-8 -*-
{
    'name': "tra_base",

    'summary': """
        Modulo en donde se encuentran los CRUDS de tablas básicas para
        el calculo de costos de los productos de la empresa textil Trapitos""",

    'description': """
        En este modulo se encuentran desarrollados los mantenimientos de tablas que contienen
        datos para el calculo de costos de la confección de prendas textiles, y que al final permitirán
        emitir un presupuesto de dicha confección a los clientes de la empresa Trapitos.
    """,

    'author': "Xavier Pacheco",
    'website': "http://www.desarrollo593.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Básica',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/tra_base_views.xml',
        'views/tra_base_actions.xml',
        'views/tra_base_menu.xml',
        'views/tra_base_templates.xml',
        # 'views/tra_configuracion_base_views.xml',
        'data/tra_gastos_config.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
