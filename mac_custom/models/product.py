# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "product.uom"

    accept_decimal = fields.Boolean('Accept Decimal')
