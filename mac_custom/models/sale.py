# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date_shipping = fields.Date(string='Shipping Date', readonly=True,
                                states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                                default=fields.Datetime.now)
    period_shipping = fields.Selection([
        ('am', 'AM'),
        ('pm', 'PM'),
        ('evening', 'Evening')],
        string='Shipping Period', copy=False)
    special_instruction = fields.Text('Message or special instructions')
