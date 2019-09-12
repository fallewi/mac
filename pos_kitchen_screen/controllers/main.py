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
        for order in request.env['pos.kitchen.order'].search([
            ('session_id', '=', session_id),
        ]):
            order_dict = {
                'id': order.id,
                'name': order.name,
                'lines': [{
                    'name': line.name,
                    'qty': line.qty,
                } for line in order.line_ids],
            }
            if order.state == 'confirmed':
                confirmed.append(order_dict)
            elif order.state == 'in_progress':
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
        order = request.env['pos.kitchen.order'].browse(int(order_id));
        if not order:
            return {'success': False, 'data': {'error': _('Could not')}}
        if order.state == 'confirmed':
            order.state = 'in_progress'
        elif order.state == 'in_progress':
            order.state = 'done'
        return {'success': True, 'data': {}}
