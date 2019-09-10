# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_kitchen_screen = fields.Boolean('Enable Kitchen Screen')

    @api.multi
    def open_kitchen_screen(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url':   '/pos/web/',
            'target': 'self',
        }
