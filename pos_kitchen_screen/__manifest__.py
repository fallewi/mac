# -*- coding: utf-8 -*-
{
    'name': 'Point of Sale - Kitchen Display',
    'category': 'Display POS orders in the kitchen',
    'summary': '',
    'website': 'https://www.microcom.ca/',
    'version': '11.0',
    'description': """
- Adds an option to the POS to be a kitchen display instead of a cashier
    """,
    'author': 'Microcom',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'templates/assets.xml',
        'templates/kitchen_screen.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
}
