# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "product.uom"

    accept_decimal = fields.Boolean('Accept Decimal')


class ProductTemplate(models.Model):
    _inherit = "product.template"

    import_sequence = fields.Char('Import Sequence')


class SaleOrder(models.Model):
    _inherit = "product.attribute"

    show_in_website = fields.Boolean('Show in website', default=True)