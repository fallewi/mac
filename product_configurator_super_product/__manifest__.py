{
    'name': 'Odoo product configurator (Super Template)',
    'category': 'product',
    'summary': 'Create template and prodct based on a super template',
    'website': 'http://www.microcom.ca',
    'version': '11.0',
    'description': """
        Super template containe all product attributes.
        """,
    'author': 'Microcom',
    'depends': ['product_configurator_wizard'],
    'data': [
        'views/sale.xml',
    ],
    'installable': True,
    'application': False,
}
