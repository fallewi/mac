{
    'name': 'Advanced Attribute Filters',
	'description': """
	Advanced Attribute Filters helps to improve the customer experience on your odoo store.
	Your customers love to find their desired products and choose products collection to save their time.
	Categorty Attributes, attribute groups , product feature , group features , 
	Website Sale Category For Attribute ,Website Product Features , Product Filter , Product Attribute
	""",
    'summary': 'Advanced Attribute Filters',
    'category': 'Website',
    'version': '1.2',
	'license' : 'OPL-1',
    'author': 'Atharva System',
    'website': 'https://www.atharvasystem.com/',
	'support': 'support@atharvasystem.com',
    'depends': ['website_sale_comparison'],
    'data': [
        'views/templates.xml', 
		'security/ir.model.access.csv'
    ],
    'images':['static/description/banner.png'],
    'installable': True,
    'price': 49.00,
    'currency': 'EUR',
    'application': True
}

