# -*- coding: utf-8 -*-
from odoo import _, http


def order_to_list(orders):
    order_list = []
    for order in orders:
        order_list.append({
            'id': order.id,
            'name': order.name,
            'lines': [{
                'name': line.product_id.name,
                'qty': line.qty,
            } for line in order.line_ids],
        })
    return order_list


class KitchenScreen(http.Controller):

    @http.route('/kitchen/screen/<int:session_id>', auth='user', type='http')
    def kitchen_screen(self, session_id, **kwargs):
        return http.request.render('pos_kitchen_screen.kitchen_orders', {'session_id': session_id})

    @http.route('/kitchen/orders/<int:session_id>', auth='user', type='json')
    def kitchen_orders(self, session_id):
        request = http.request
        confirmed = order_to_list(request.env['pos.kitchen.order'].search([
            ('session_id', '=', session_id),
            ('state', '=', 'confirmed'),
        ]))
        in_progress = order_to_list(request.env['pos.kitchen.order'].search([
            ('session_id', '=', session_id),
            ('state', '=', 'in_progress'),
        ]))
        done = order_to_list(request.env['pos.kitchen.order'].search([
            ('session_id', '=', session_id),
            ('state', '=', 'done'),
        ], order='write_date desc'))
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

    @http.route('/kitchen/update_order', auth='user', type='json')
    def new_order(self, **kwargs):
        if 'name' not in kwargs or 'session_id' not in kwargs:
            return {'success': False}

        request = http.request
        session_id = kwargs['session_id']
        order_ref = kwargs['name']
        linked_orders = request.env['pos.kitchen.order'].search([
            ('session_id', '=', session_id),
            ('reference', '=', order_ref),
        ])
        existing_confirmed_order = linked_orders.filtered(lambda o: o.state == 'confirmed')
        if kwargs.get('new'):
            order_lines = [(0, 0, {
                'product_id': line['id'],
                'qty': line['qty'],
            }) for line in kwargs['new']]
            # Update existing confirmed order
            if existing_confirmed_order:
                existing_confirmed_order.write({'line_ids': order_lines})
            else:
                name = order_ref
                if linked_orders:
                    name = '%s - %d' % (name, len(linked_orders) + 1)
                request.env['pos.kitchen.order'].create({
                    'name': name,
                    'reference': order_ref,
                    'session_id': session_id,
                    'state': 'confirmed',
                    'line_ids': order_lines,
                })
        if kwargs.get('cancelled') and existing_confirmed_order:
            for cancel_line in kwargs['cancelled']:
                for line in existing_confirmed_order.line_ids:
                    if line.product_id.id == cancel_line['id'] and line.qty >= cancel_line['qty']:
                        if line.qty == cancel_line['qty']:
                            line.unlink()
                        else:
                            line.qty -= cancel_line['qty']
                        break
            
            if not existing_confirmed_order.line_ids:
                existing_confirmed_order.unlink()

        return {'success': True}
