# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    sale_price = fields.Float(string='Sale Price', compute='_compute_sale_price', inverse='_set_product_lst_price',
                              digits=dp.get_precision('Product Price'))
    profit_percentage = fields.Float(string='% profit', compute='_compute_profit_percentage',
                                     digits=dp.get_precision('Product Price'))
    available_in_pos = fields.Boolean(string='POS', related='product_id.available_in_pos')
    website_published = fields.Boolean(string='ecommerce', related='product_id.website_published')

    @api.depends('product_id')
    def _compute_sale_price(self):
        self.sale_price = self.product_id.lst_price

    def _set_product_lst_price(self):
        self.product_id.lst_price = self.sale_price

    @api.depends('product_id', 'sale_price', 'price_unit')
    def _compute_profit_percentage(self):
        profit = self.sale_price - self.price_unit
        if self.price_unit != 0:
            self.profit_percentage = profit / self.price_unit * 100
        else:
            self.profit_percentage = 0

    def button_purchase_info(self):
        view_id = self.env.ref('mac_custom.purchase_order_line_info_view').id
        wiz = self.env['purchase.order.line.info'].create({
            'order_line_id': self.id,
            'product_id': self.product_id.id})
        return {
            'name': _('Product Information'),
            'view_mode': 'readonly',
            'view_type': 'form',
            'res_model': 'purchase.order.line.info',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': wiz.id,
            'target': 'new',
            'flags': {'initial_mode': 'readonly'}
        }

    @api.onchange('website_published')
    def onchange_website_published(self):
        if self.website_published and self.sale_price == 0:
            raise UserError(_("Can not activate website if sale price is not defined."))

    @api.onchange('available_in_pos')
    def onchange_website_published(self):
        if self.available_in_pos and self.sale_price == 0:
            raise UserError(_("Can not activate POS if sale price is not defined."))
