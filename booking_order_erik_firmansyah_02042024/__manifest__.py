# -*- coding: utf-8 -*-
{
    'name': 'Booking Order',
    'version': '1.0.1',
    'author': 'Erik Firmansyah',
    'category': 'sale',
    'maintainer': 'Erik Firmansyah',
    'summary': """Booking Order""",
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/work_order_template.xml',
        'data/ir_sequence.xml',
        'views/service_team_views.xml',
        'views/work_order_views.xml',
        'views/booking_order_views.xml',
        'views/sale_order_views.xml',
        'views/menu_items.xml',
        'wizard/popup_message_wizard_views.xml',
        'wizard/cancel_work_order_wizard_views.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}