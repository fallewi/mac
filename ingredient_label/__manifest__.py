# -*- coding: utf-8 -*-
{
    'name': 'Ingredient Label',
    'version': '1.0',
    'author': 'Microcom',
    'category': '',
    'summary': '',
    'description': """
    """,
    'depends': ['point_of_sale', 'printer_zpl2', 'product_expiry'],
    'data': [
        'wizard/create_lot_views.xml',
        'views/product_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_production_lot_views.xml',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
