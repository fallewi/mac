# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    order_state = fields.Selection([
        ('draft', _('Draft')),
        ('confirmed', _('Confirmed')),
        ('in_progress', _('In Progress')),
        ('done', _('Done')),
    ], 'Order State', default='draft')
