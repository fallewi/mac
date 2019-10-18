# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models
from datetime import timedelta


class BookingTable(models.Model):
    _name = 'booking.table'
    _description = 'Booking Table'

    name = fields.Char('Name', required=True)
    booking_ids = fields.One2many('booking.booking', 'table_id', 'Bookings')


class BookingMenu(models.Model):
    _name = 'booking.menu'
    _description = 'Booking Menu'

    name = fields.Char('Name', required=True)
    description = fields.Html('Description')


class BookingLine(models.Model):
    _name = 'booking.line'
    _description = 'Amount of menus booked'

    menu_id = fields.Many2one('booking.menu', 'Menu', required=True)
    booking_id = fields.Many2one('booking.booking', 'Booking', required=True)
    quantity = fields.Integer('Quantity', required=True, default=1)


class BookingBooking(models.Model):
    _name = 'booking.booking'
    _inherit = ['mail.thread']
    _description = 'Booking'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    email = fields.Char(related='partner_id.email')
    phone = fields.Char(related='partner_id.phone')
    mobile = fields.Char(related='partner_id.mobile')
    table_id = fields.Many2one('booking.table', 'Table')
    line_ids = fields.One2many('booking.line', 'booking_id', 'Menus')
    date = fields.Datetime('Date', required=True)
    notes = fields.Text('Notes')
    state = fields.Selection([
        ('new', _('New')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
    ], 'State', default='new', required=True, track_visibility='onchange')
    end_date = fields.Datetime('End Date')

    @api.model
    def default_get(self, fields_list):
        res = super(BookingBooking, self).default_get(fields_list)
        if self.env.context.get('default_name') and not res.get('partner_id'):
            partner = self.env['res.partner'].search(
                [('name', 'ilike', self.env.context['default_name'])], limit=1)
            if partner:
                res['partner_id'] = partner.id
        return res

    @api.multi
    @api.constrains('date', 'end_date', 'table_id')
    def check_table_availability(self):
        for booking in self:
            if booking.table_id and self.search([
                ('id', '!=', booking.id),
                ('table_id', '=', booking.table_id.id),
                '|',
                '&',
                ('date', '>=', booking.date),
                ('date', '<', booking.end_date),
                '&',
                ('end_date', '>', booking.date),
                ('end_date', '<=', booking.end_date),
            ]):
                raise exceptions.ValidationError(_(
                    'The table %s has already been booked for this time' % booking.table_id.name))

    @api.multi
    @api.depends('partner_id', 'table_id')
    def name_get(self):
        result = []
        for booking in self:
            if booking.table_id:
                name = '%s - %s' % (booking.table_id.name, booking.partner_id.name)
            else:
                name = booking.partner_id.name
            result.append((booking.id, name))
        return result
