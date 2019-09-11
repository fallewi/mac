# -*- coding: utf-8 -*-
from odoo import _, http


class KitchenScreen(http.Controller):
    @http.route('/kitchen/screen/<int:session_id>', auth='user', type='http')
    def kitchen_screen(self, session_id, **kwargs):
        return http.request.render('pos_kitchen_screen.kitchen_orders', {'session_id': session_id})

    @http.route('/kitchen/orders/<int:session_id>', auth='user', type='json')
    def kitchen_orders(self, session_id):
        request = http.request
        confirmed = []
        in_progress = []
        done = []
        for order in request.env['pos.order'].search([
            ('session_id', '=', session_id),
            ('order_state', '!=', 'draft'),
        ]):
            order_dict = {
                'id': order.id,
                'name': order.name,
                'lines': [{
                    'product_name': line.product_id.name,
                    'qty': line.qty,
                } for line in order.lines],
            }
            if order.order_state == 'confirmed':
                confirmed.append(order_dict)
            elif order.order_state == 'in_progress':
                in_progress.append(order_dict)
            else:
                done.append(order_dict)
        return {'success': True, 'data': {
            'confirmed': confirmed,
            'in_progress': in_progress,
            'done': done,
        }}

    @http.route('/kitchen/order_next_step/<int:order_id>', auth='user', type='json')
    def order_next_step(self, order_id):
        request = http.request
        order = request.env['pos.order'].browse(int(order_id));
        if not order:
            return {'success': False, 'data': {'error': _('Could not')}}
        if order.order_state == 'confirmed':
            order.order_state = 'in_progress'
        elif order.order_state == 'in_progress':
            order.order_state = 'done'
        return {'success': True, 'data': {}}
