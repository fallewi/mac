# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp


class POSKitchenOrder(models.Model):
    _name = 'pos.kitchen.order'
    _description = 'Kitchen Order'

    def _default_session(self):
        return self.env['pos.session'].search([
            ('state', '=', 'opened'), ('user_id', '=', self.env.uid)
        ], limit=1)

    name = fields.Char('Order Name')
    line_ids = fields.One2many('pos.kitchen.order.line', 'order_id', 'Lines')
    session_id = fields.Many2one(
        'pos.session', string='Session', required=True, index=True,
        domain="[('state', '=', 'opened')]", states={'draft': [('readonly', False)]},
        readonly=True, default=_default_session)
    state = fields.Selection([
        ('confirmed', _('Confirmed')),
        ('in_progress', _('In Progress')),
        ('done', _('Done')),
    ], 'State', default='confirmed')


class POSKitchenOrderLine(models.Model):
    _name = 'pos.kitchen.order.line'
    _description = 'Kitchen Order'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product')
    order_id = fields.Many2one('pos.kitchen.order', 'Kitchen Order')
    qty = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'))
