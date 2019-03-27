# -*- coding: utf-8 -*-

import datetime

from odoo import fields, models


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    description = fields.Text('Description')

    def _get_dates(self, product_id=None):
        """Returns dates based on number of days configured in current lot's product."""
        mapped_fields = {
            'life_date': 'life_time',
            'use_date': 'use_time',
            'removal_date': 'removal_time',
            'alert_date': 'alert_time'
        }
        mapped_variant_fields = {
            'life_date': 'life_variant_time',
            'use_date': 'use_variant_time',
            'removal_date': 'removal_variant_time',
            'alert_date': 'alert_variant_time'
        }
        res = dict.fromkeys(mapped_fields, False)
        product = self.env['product.product'].browse(product_id) or self.product_id
        if product:
            for field in mapped_fields:
                duration = getattr(product, mapped_variant_fields[field])
                if duration == 0:
                    duration = getattr(product, mapped_fields[field])
                if duration:
                    date = datetime.datetime.now() + datetime.timedelta(days=duration)
                    res[field] = fields.Datetime.to_string(date)
        return res
