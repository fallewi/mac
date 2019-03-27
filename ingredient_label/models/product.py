# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    ingredients = fields.Text('Ingredients')
    life_variant_time = fields.Integer(
        string='Variant Life Time',
        help='Number of days before the goods may become dangerous and must not be consumed. It will be computed on the lot/serial number.')
    use_variant_time = fields.Integer(
        string='Variant Use Time',
        help='Number of days before the goods starts deteriorating, without being dangerous yet. It will be computed on the lot/serial number.')
    removal_variant_time = fields.Integer(
        string='Variant Removal Time',
        help='Number of days before the goods should be removed from the stock. It will be computed on the lot/serial number.')
    alert_variant_time = fields.Integer(
        string='Variant Alert Time',
        help='Number of days before an alert should be raised on the lot/serial number.')
