
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class ProductFilterGroup(models.Model):
    _name = "product.filter.group"
    _description = "Product Filters Group"
    _order = 'sequence, name'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    filter_ids = fields.One2many('product.filter', 'group_id', 'Values', copy=True)



class ProductFilters(models.Model):
    _name = "product.filter"
    _description = "Product Filters"
    _order = 'sequence, name'

    name = fields.Char('Name', required=True, translate=True)
    group_id = fields.Many2one('product.filter.group', string="Group")    
    value_ids = fields.One2many('product.filter.value', 'filter_id', 'Values', copy=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    filter_line_ids = fields.One2many('product.filter.line', 'filter_id', 'Lines')
    create_variant = fields.Boolean(default=True, help="Check this if you want to create multiple variants for this filter.")
    type = fields.Selection([('radio', 'Radio'), ('select', 'Select'), ('color', 'Color'), ('hidden', 'Hidden')], default='radio')

    _sql_constraints = [
        ('value_filter_uniq', 'unique (name,group_id)', 'This filter already exists !')
    ]

class ProductFiltervalue(models.Model):
    _name = "product.filter.value"
    _order = 'sequence'

    name = fields.Char('Value', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    filter_id = fields.Many2one('product.filter', 'Filter', ondelete='cascade', required=True)
    product_ids = fields.Many2many('product.product', id1='att_id', id2='prod_id', string='Variants', readonly=True)
    html_color = fields.Char(string='HTML Color Index', oldname='color', help="Here you can set a "
                             "specific HTML color index (e.g. #ff0000) to display the color on the website if the "
                             "attibute type is 'Color'.")
    _sql_constraints = [
        ('value_filter_val_uniq', 'unique (name,filter_id)', 'This filter value already exists !')
    ]
class ProductfilterLine(models.Model):
    _name = "product.filter.line"
    _rec_name = 'filter_id'

    product_tmpl_id = fields.Many2one('product.template', 'Product Template', ondelete='cascade', required=True)
    filter_id = fields.Many2one('product.filter', 'Filter', ondelete='restrict', required=True)
    value_ids = fields.Many2many('product.filter.value', id1='line_id', id2='val_id', string='Filter Values')

    @api.constrains('value_ids', 'filter_id')
    def _check_valid_filter(self):
        if any(line.value_ids > line.filter_id.value_ids for line in self):
            raise ValidationError(_('Error ! You cannot use this filter with the following value.'))
        return True

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        # TDE FIXME: currently overriding the domain; however as it includes a
        # search on a m2o and one on a m2m, probably this will quickly become
        # difficult to compute - check if performance optimization is required
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            new_args = ['|', ('attrib_id', operator, name), ('value_ids', operator, name)]
        else:
            new_args = args
        return super(ProductfilterLine, self).name_search(name=name, args=new_args, operator=operator, limit=limit)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    filter_line_ids = fields.One2many('product.filter.line', 'product_tmpl_id', 'Product Filters')

    @api.constrains('filter_line_ids')
    def _check_filter_value_ids(self):
        for product in self:
            filters = self.env['product.filter']
            for value in product.filter_line_ids:
                if value.filter_id in filters:
                    raise ValidationError(_('Error! It is not allowed to choose more than one value for a given filter.'))
                filters |= value.filter_id
        return True
