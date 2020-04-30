# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Roberto Barreiro (<roberto@disgal.es>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'eCommerce With Uom',
    'version': '11',
    'depends': ['website_sale',],
    'author': 'Roberto Barreiro',
    'website': 'https://bitbucket.org/disgalmilladoiro/',
    'summary': 'Show product unit of measure on shop.',
    'description': '''
    Adds Uom next to the product price at shop and shopping cart.

    REQUIRED: You may grant portal and public groups to read product.uom model or will be an access error for users of this groups.

    ''',
    'category': 'eCommerce',
    'sequence': 10,
    'data': [
        'security/ir.model.access.csv',
        'views/website_sale_show_uom.xml',],
    'images': ['static/description/banner.png',],
    'installable': True,
    'auto_install': False,
    'application': False,
}
