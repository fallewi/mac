{
    'name': 'ecommerce sold out',
    'category': 'Website',
    'summary': 'Add ribon "Sold Out" if product is out of stock',
    'website': 'http://www.microcom.ca',
    'version': '11.0',
    'description': """
        Add ribbon to product list if product is out of stock
        """,
    'author': 'Microcom',
    'depends': ['website_sale'],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
}
