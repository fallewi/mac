# -*- coding: utf-8 -*-
from odoo import _, api, exceptions, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_kitchen_screen = fields.Boolean('Enable Kitchen Screen')

    @api.multi
    def open_kitchen_screen(self):
        self.ensure_one()
        if not self.current_session_id:
            raise exceptions.UserError(_('Open a session before opening the kitchen screen'))
        return {
            'type': 'ir.actions.act_url',
            'url':   '/kitchen/screen/%d' % self.current_session_id.id,
            'target': 'self',
        }
