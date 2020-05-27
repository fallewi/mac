# -*- coding: utf-8 -*-

from lxml import etree

from odoo.osv import orm
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProductConfigurator(models.TransientModel):
    _inherit = "product.configurator"

    def unmerged_values(self, value_ids):
        for value_id in value_ids:
            if value_id.merged_value_ids:
                value_ids -= value_id
                for merged_value_id in value_id.merged_value_ids:
                    value_ids += merged_value_id
        return value_ids

    @api.model
    def create(self, vals):
        res = super(ProductConfigurator, self).create(vals)
        if vals.get('product_id'):
            product = self.env['product.product'].browse(vals['product_id'])
            res.product_tmpl_id = product.super_template or product.product_tmpl_id
            if product.super_template:
                res.value_ids = self.unmerged_values(res.value_ids)

        return res

    @api.multi
    def action_config_done(self):
        """Parse values and execute final code before closing the wizard"""
        custom_vals = {
            l.attribute_id.id:
                l.value or l.attachment_ids for l in self.custom_value_ids
        }

        # This try except is too generic.
        # The create_variant routine could effectively fail for
        # a large number of reasons, including bad programming.
        # It should be refactored.
        # In the meantime, at least make sure that a validation
        # error legitimately raised in a nested routine
        # is passed through.
        try:
            # - create when reusable, will reuse matching instead of creating duplicate
            # - update when modifiable, will change current variant instead of picking/creating new one
            duplicates = self.product_tmpl_id.find_duplicates(self.value_ids.ids, custom_vals, product_id=self.product_id)
            if self.product_id:
                # used cogs icon (or selected variant in first step)
                variant = self.product_id
                if variant in duplicates:
                    # no change, leave as is
                    pass
                elif not self.product_modifiable:
                    variant = self.product_tmpl_id.create_get_variant(
                        self.value_ids.ids, custom_vals)
                elif duplicates and self.product_reusable:
                    # variant duplicates another product, warn user
                    raise ValidationError(
                        _('Duplicate configuration! Variant already exists (id={})').format(duplicates[0].id)
                    )
                else:
                    # Begin changes
                    # modify current variant
                    self.product_id.product_tmpl_id.config_ok = True
                    self.product_id.product_tmpl_id.update_template_attribute(
                        self.product_id.product_tmpl_id.merge_multi_value(self.value_ids.ids))

                    vals = self.product_tmpl_id.get_update_variant_vals(self.value_ids.ids, custom_vals)
                    if vals.get('attribute_value_ids'):
                        vals['attribute_value_ids'] = [(6, 0, variant.product_tmpl_id.merge_multi_value(
                            vals.get('attribute_value_ids')[0][2]))]
                    variant.write(vals)
                    variant.change_all_name()
                    self.product_id.product_tmpl_id.config_ok = False
                    # End changes
            else:
                if duplicates and self.product_reusable and self.product_force_create:
                    # variant duplicates another product, warn user
                    raise ValidationError(
                        _('Duplicate configuration! Variant already exists (id={})').format(duplicates[0].id)
                    )
                # creating new SO line
                if self.product_reusable:
                    variant = self.product_tmpl_id.create_get_variant(
                        self.value_ids.ids, custom_vals)
                else:
                    # create a new variant
                    vals = self.product_tmpl_id.get_variant_vals(self.value_ids.ids, custom_vals)
                    variant = self.env['product.product'].create(vals)
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(
                _('Invalid configuration! Please check all '
                  'required steps and fields. ')
            )

        self.action_config_done_postprocess(variant)
        self.unlink()