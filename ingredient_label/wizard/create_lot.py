# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CreateLot(models.TransientModel):
    _name = 'ingredient_label.create.lot'
    _description = 'Create Lot'

    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('type', 'in', ['product', 'consu'])], required=True)
    product_uom_qty = fields.Float('Quantity', default=1)
    product_uom_id = fields.Many2one(related='product_id.uom_id')
    lot_qty = fields.Integer('Lot Count', default=1)
    print_label = fields.Boolean('Print Label')
    printer_id = fields.Many2one(
        comodel_name='printing.printer', string='Printer',
        help='Printer used to print the labels.')
    label_id = fields.Many2one(
        comodel_name='printing.label.zpl2', string='Label',
        domain=[('model_id.model', '=', 'stock.production.lot')],
        help='Label to print.')

    @api.model
    def default_get(self, fields_list):
        # copied from PrintRecordLabel in module printer_zpl2
        values = super(CreateLot, self).default_get(fields_list)

        # Automatically select the printer and label, if only one is available
        printers = self.env['printing.printer'].search(
            [('id', '=', self.env.context.get('printer_zpl2_id'))])
        if not printers:
            printers = self.env['printing.printer'].search([('default', '=', True)])
        if not printers:
            printers = self.env['printing.printer'].search([])
        if len(printers) == 1:
            values['printer_id'] = printers.id

        labels = self.env['printing.label.zpl2'].search([
            ('model_id.model', '=', 'stock.production.lot')])
        if len(labels) == 1:
            values['label_id'] = labels.id

        return values

    def process(self):
        move_id = self.env['stock.move'].browse(self.env.context['active_id'])
        for i in range(self.lot_qty):
            lot_id = self.env['stock.production.lot'].create({
                'name': self.env['ir.sequence'].next_by_code('stock.lot.serial'),
                'product_id': self.product_id.id,
            })
            move_line = self.env['stock.move.line'].create({
                'lot_id': lot_id.id,
                'lot_name': lot_id.name,
                'move_id': move_id.id,
                'qty_done': self.product_uom_qty,
                'product_uom_id': self.product_uom_id.id,
                'picking_id': move_id.picking_id.id,
                'location_id': move_id.location_id.id,
                'location_dest_id': move_id.location_dest_id.id,
                'owner_id': move_id.picking_id.owner_id.id,
            })
            if self.print_label:
                self.label_id.print_label(self.printer_id, move_line.lot_id)
        return False
