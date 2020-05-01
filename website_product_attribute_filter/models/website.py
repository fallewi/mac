# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError
import openerp
from openerp.http import request
from openerp.addons.website.models.website import slugify


class website(models.Model):

    """Adds the fields for group filter."""

    _inherit = 'website'

    disable_group_filter = fields.Boolean(string="Do you want to disable Feature Group Feature?")
    disable_count_filter = fields.Boolean(string="Do you want to disable Product Count?")

class WebsiteConfigSettings(models.TransientModel):

    """Settings for the group filter."""

    _inherit = 'res.config.settings'


    disable_group_filter = fields.Boolean(string="Do you want to disable Feature Group Feature?", related='website_id.disable_group_filter',store=True,)
    disable_count_filter = fields.Boolean(string="Do you want to disable Product Count?", related='website_id.disable_count_filter',store=True,)
