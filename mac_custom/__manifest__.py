# -*- coding: utf-8 -*-
{
    'name': 'Mante du Caré Custom',
    'version': '11.0',
    'author': 'Microcom',
    'category': '',
    'summary': '',
    'description': """
        Traduction personnalisé et changement mineur.
    """,
    'depends': ['website_sale', 'ingredient_label', 'website_product_attribute_filter', 'website_sale_delivery'],
    'data': [
        "views/product.xml",
        "views/sale.xml",
        "views/website_sale.xml",
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
