# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import Controller, request, route
from odoo import http
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

period_shipping = [
    ('am', 'AM'),
    ('pm', 'PM'),
    ('evening', _('Evening'))
]

class CustomerPortal(CustomerPortal):

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        response = super().account(redirect=redirect, **post)

        # remove VAT field from /my/account form
        response.qcontext.pop('has_check_vat')
        return response


class WebsiteSaleDelivery(WebsiteSaleDelivery):

    def _get_shop_payment_values(self, order, **kwargs):
        values = super(WebsiteSaleDelivery, self)._get_shop_payment_values(order, **kwargs)

        if values.get('delivery_has_stockable'):
            values['periods'] = period_shipping

        return values

    @route(['/shop/update_shipping_info'], type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def update_eshop_shipping_info(self, **post):
        values = {}
        order = request.website.sale_get_order()

        if order:
            values.update({'date_shipping': post.get('date_shipping') or order.date_shipping})
            values.update({'period_shipping': post.get('period_shipping') or order.period_shipping})
            values.update({'special_instruction': post.get('special_instruction') or order.special_instruction})
            order.write(values)

        return values

    @route(['/shop/payment'], type='http', auth="public", website=True, sitemap=False)
    def payment(self, **post):
        order = request.website.sale_get_order()
        if order:
            order.date_shipping = post.get('date_shipping') or order.date_shipping
            order.period_shipping = post.get('period_shipping') or order.period_shipping
            order.special_instruction = post.get('special_instruction') or order.special_instruction

        return super().payment(**post)


class WebsiteSale(WebsiteSale):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSale, self).shop(page, category, search, ppg, **post)

        domain = self._get_search_domain(search, category, res.qcontext.get('attrib_values'))
        Product = request.env['product.template']
        ProductAttributeline = request.env['product.attribute.line']
        if res.qcontext.get('products'):
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttributeline.search([('product_tmpl_id', 'in', selected_products.ids),
                                                      ('value_ids', '!=', False)]).mapped('attribute_id').sorted(lambda r: (r.sequence, r.name))
        else:
            attributes = res.qcontext.get('attributes')

        res.qcontext['attributes'] = attributes
        return res
