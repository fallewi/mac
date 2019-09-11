# -*- coding: utf-8 -*-
from odoo import http


class KitchenScreen(http.Controller):
    @http.route('/kitchen/orders/<int:config_id>', auth='user', type='http')
    def kitchen_orders(self, config_id, **kwargs):
        return http.request.render('pos_kitchen_screen.kitchen_orders', {})
