# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PurchaseOrderLineInfo(models.TransientModel):
    _name = 'purchase.order.line.info'
    _description = 'Product information'

    order_line_id = fields.Many2one('purchase.order.line')
    product_id = fields.Many2one('product.product', 'Product')
    qty_available = fields.Float('Quantity On Hand', related='product_id.qty_available')
    virtual_available = fields.Float('Forecast Quantity', related='product_id.virtual_available')
    incoming_qty = fields.Float('Incoming Quantity', related='product_id.incoming_qty')
    outgoing_qty = fields.Float('outgoing Quantity', related='product_id.outgoing_qty')

