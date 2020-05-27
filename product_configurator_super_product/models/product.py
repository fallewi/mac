# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    super_template = fields.Many2one('product.template', domain="[('config_ok', '=', True)]")

    @api.multi
    def search_variant(self, value_ids, custom_values=None):
        """ Searches product.variants with given value_ids and custom values
            given in the custom_values dict

            :param value_ids: list of product.attribute.values ids
            :param custom_values: dict {product.attribute.id: custom_value}

            :returns: product.product recordset of products matching domain
        """
        self.ensure_one()

        # TODO search finds any match with same 2+ custom attributes

        if custom_values is None:
            custom_values = {}
        attr_obj = self.env['product.attribute']

        domain = [('product_tmpl_id.super_template', '=', self.id)]

        for value_id in value_ids:
            domain.append(('attribute_value_ids', '=', value_id))

        attr_search = attr_obj.search([
            ('search_ok', '=', False),
            ('custom_type', 'not in', attr_obj._get_nosearch_fields())
        ])

        for attr_id, value in custom_values.items():
            if attr_id not in attr_search.ids:
                domain.append(
                    ('value_custom_ids.attribute_id', '!=', int(attr_id)))
            else:
                domain.append(
                    ('value_custom_ids.attribute_id', '=', int(attr_id)))
                domain.append(('value_custom_ids.value', '=', value))

        products = self.env['product.product'].search(domain)

        # At this point, we might have found products with all of the passed
        # in values, but it might have more attributes!  These are NOT
        # matches
        more_attrs = products.filtered(
            lambda p:
            len(p.attribute_value_ids) != len(value_ids) or
            len(p.value_custom_ids) != len(custom_values)
            )
        products -= more_attrs
        return products

    @api.multi
    def get_attribute_vals(self, value_ids):
        self.ensure_one()

        attrib = []
        for value in self.env['product.attribute.value'].browse(value_ids):
            attrib.append((0, 0, {'attribute_id': value.attribute_id.id,
                                  'value_ids': [(6, 0, value.ids)]}))
        return attrib

    @api.multi
    def merge_multi_value(self, value_ids):
        self.ensure_one()

        attribute = []
        multi_attribute = []

        attribute_value_ids = self.env['product.attribute.value'].browse(value_ids)

        for value in attribute_value_ids:

            if value.attribute_id in attribute:
                if value.attribute_id not in multi_attribute:
                    multi_attribute.append(value.attribute_id)
            else:
                attribute.append(value.attribute_id)


        for attribute in multi_attribute:
            attribute_name = ""
            merged_value_ids = []
            loc = 0
            for value in attribute_value_ids:
                if value.attribute_id == attribute:
                    if attribute_name != "":
                        attribute_name += ", "
                    attribute_name += value.name
                    loc = value_ids.index(value.id)
                    merged_value_ids.append(value.id)
                    value_ids.remove(value.id)
            attribute_value_id = self.env['product.attribute.value'].search([('attribute_id', '=', attribute.id),
                                                                             ('name', '=', attribute_name)])
            if not attribute_value_id:
                context = self._context.copy()
                context['no_template'] = True
                vals = {
                    'attribute_id': attribute.id,
                    'name': attribute_name,
                    'merged_value_ids': [(6, 0, merged_value_ids)]
                }
                attribute_value_id = self.with_context(context).env['product.attribute.value'].create(vals)
            elif not attribute_value_id.merged_value_ids:
                vals = {
                    'merged_value_ids': [(6, 0, merged_value_ids)]
                }
                attribute_value_id.update(vals)

            value_ids.insert(loc, attribute_value_id.id)

        return value_ids

    @api.multi
    def get_variant_vals(self, template, value_ids, custom_values=None, **kwargs):
        """ Hook to alter the values of the product variant before creation

            :param value_ids: list of product.attribute.values ids
            :param custom_values: dict {product.attribute.id: custom_value}

            :returns: dictionary of values to pass to product.create() method
         """
        self.ensure_one()

        image = self.get_config_image_obj(value_ids).image
        all_images = tools.image_get_resized_images(
            image, avoid_resize_medium=True)
        vals = {
            'product_tmpl_id': template.id,
            'super_template': self.id,
            'attribute_value_ids': [(6, 0, value_ids)],
            'taxes_id': [(6, 0, self.taxes_id.ids)],
            'image': image,
            'image_variant': image,
            'image_medium': all_images['image_medium'],
            'image_small': all_images['image_medium'],
        }

        if custom_values:
            vals.update({
                'value_custom_ids': self.encode_custom_values(custom_values)
            })

        return vals

    @api.multi
    def create_get_variant(self, value_ids, custom_values=None):
        """ Creates a new product variant with the attributes passed via value_ids
        and custom_values or retrieves an existing one based on search result

            :param value_ids: list of product.attribute.values ids
            :param custom_values: dict {product.attribute.id: custom_value}

            :returns: new/existing product.product recordset

        """
        if custom_values is None:
            custom_values = {}
        valid = self.validate_configuration(value_ids, custom_values)
        if not valid:
            raise ValidationError(_('Invalid Configuration'))

        duplicates = self.search_variant(value_ids,
                                         custom_values=custom_values)

        # At the moment, I don't have enough confidence with my understanding
        # of binary attributes, so will leave these as not matching...
        # In theory, they should just work, if they are set to "non search"
        # in custom field def!
        # TODO: Check the logic with binary attributes
        if custom_values:
            value_custom_ids = self.encode_custom_values(custom_values)
            if any('attachment_ids' in cv[2] for cv in value_custom_ids):
                duplicates = False

        if duplicates:
            return duplicates[0]

        value_ids = self.merge_multi_value(value_ids)

        vals = {
            'name': '__temp__',  # Must have a name initial, renamed later
            'sequence': 10,
            'type': self.type,
            'categ_id': self.categ_id.id,
            'list_price': self.list_price,
            'sale_ok': self.sale_ok,
            'purchase_ok': self.purchase_ok,
            'uom_id': self.uom_id.id,
            'uom_po_id': self.uom_po_id.id,
            'compagny_id': self.company_id.id,
            'active': self.active,
            'config_ok': True,      # Do not create variant automatically
            'super_template': self.id,
            'attribute_line_ids': self.get_attribute_vals(value_ids)
        }

        # variant = self.env['product.product'].create(vals)
        # variant.name = variant.get_config_variant_name()
        template = self.env['product.template'].create(vals)

        vals = self.get_variant_vals(template, value_ids, custom_values)
        variant = self.env['product.product'].create(vals)

        variant.change_all_name()

        template.config_ok = False

        return variant

    @api.multi
    def update_template_attribute(self, value_ids):
        self.ensure_one()

        # Remove current variant
        self.write({'attribute_line_ids': [(5,)]})

        # Add new variant
        vals = {
            'attribute_line_ids': self.get_attribute_vals(value_ids)
        }
        # Update template attributes list.
        self.write(vals)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def change_all_name(self):
        all_lang = self.env['res.lang'].search([('active', '=', True)]).mapped('code')
        for lang in all_lang:
            context = dict(self.env.context)
            context.update({'lang': lang})
            self.product_tmpl_id.with_context(context).name = "__temp__"
            self.product_tmpl_id.with_context(context).name = self.with_context(context).display_name.replace("__temp__, ", "")

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    merged_value_ids = fields.Many2many(comodel_name='product.attribute.value', relation='merged_attribute_rel',
                                        column1='merged_value_id', column2='parent_merged_id',
                                        string='Merged value')

    def _set_price_extra(self):
        if self._context.get('no_template'):
            return

        return super(ProductAttributeValue, self)._set_price_extra()