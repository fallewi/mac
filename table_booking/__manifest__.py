# -*- coding: utf-8 -*-
{
    'name': 'Table Booking',
    'category': 'Bookings',
    'summary': 'Table Booking Application',
    'website': 'https://www.microcom.ca/',
    'version': '11.0',
    'description': """
This module allows to manage table bookings
    """,
    'author': 'Microcom',
    'depends': [
        'mail',
    ],
    'data': [
        'security/booking_booking_security.xml',
        'security/ir.model.access.csv',
        'views/booking_booking.xml',
    ],
    'installable': True,
    'application': True,
}
