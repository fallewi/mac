# -*- coding: utf-8 -*-
{
    'name': 'Point of Sale - Kitchen Display',
    'category': 'Point of Sale',
    'summary': 'Display POS orders in the kitchen',
    'website': 'https://www.microcom.ca/',
    'version': '11.0',
    'description': """
- Adds an option to the POS to be a kitchen display instead of a cashier
    """,
    'author': 'Microcom',
    'depends': [
        'pos_restaurant',
    ],
    'data': [
        'security/ir.model.access.csv',
        'templates/assets.xml',
        'templates/kitchen_screen.xml',
        'views/pos_config.xml',
        'views/pos_kitchen_order.xml',
    ],
    'qweb': [
        'static/src/xml/pos_send_orders_button.xml',
    ],
    'installable': True,
    'application': False,
}
