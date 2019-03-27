odoo.define('pos_untaxed.models', function (require) {
"use strict";

var models = require('point_of_sale.models');
var utils = require('web.utils');

var round_pr = utils.round_precision;

models.Order = models.Order.extend({
    get_taxed_subtotal: function() {
        return round_pr(this.orderlines.filter(line => line.get_tax() !== 0)
            .reduce((function(sum, orderLine) {
                return sum + orderLine.get_price_without_tax();
            }), 0), this.pos.currency.rounding);
    },
    get_untaxed_subtotal: function() {
        return round_pr(this.orderlines.filter(line => line.get_tax() === 0)
            .reduce((function(sum, orderLine) {
                return sum + orderLine.get_price_without_tax();
            }), 0), this.pos.currency.rounding);
    },
});

models.PosModel = models.PosModel.extend({
    models: models.PosModel.prototype.models.concat({
        model:  'stock.production.lot',
        fields: ['name','product_id'],
        domain: [['product_id.sale_ok','=',true],['product_id.available_in_pos','=',true]],
        loaded: function(self,lots){
            _.each(lots, function (lot) {
                var product = self.db.get_product_by_id(lot.product_id[0]);
                self.db.product_by_barcode[lot.name] = product;
            })
        }
    }),
    scan_product: function(parsed_code){
        var selectedOrder = this.get_order();
        var product = this.db.get_product_by_barcode(parsed_code.base_code);

        if(!product){
            return false;
        }

        if(parsed_code.type === 'price'){
            selectedOrder.add_product(product, {price:parsed_code.value});
        }else if(parsed_code.type === 'weight'){
            selectedOrder.add_product(product, {quantity:parsed_code.value, merge:false});
        }else if(parsed_code.type === 'discount'){
            selectedOrder.add_product(product, {discount:parsed_code.value, merge:false});
        }else if(product.tracking !== 'none' && this.config.use_existing_lots){
            selectedOrder.add_product(product, {lot:parsed_code.base_code});
        }else{
            selectedOrder.add_product(product);
        }
        return true;
    },
})

models.Order = models.Order.extend({
    add_product: function(product, options){
        if(this._printed){
            this.destroy();
            return this.pos.get_order().add_product(product, options);
        }
        this.assert_editable();
        options = options || {};
        var attr = JSON.parse(JSON.stringify(product));
        attr.pos = this.pos;
        attr.order = this;
        var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});

        if(options.quantity !== undefined){
            line.set_quantity(options.quantity);
        }

        if(options.price !== undefined){
            line.set_unit_price(options.price);
        }

        //To substract from the unit price the included taxes mapped by the fiscal position
        this.fix_tax_included_price(line);

        if(options.discount !== undefined){
            line.set_discount(options.discount);
        }

        if(options.extras !== undefined){
            for (var prop in options.extras) {
                line[prop] = options.extras[prop];
            }
        }

        if(options.lot !== undefined){
            if(line.has_product_lot && product.barcode !== options.lot){
                var pack_lot_line = new models.Packlotline({}, {'order_line':line});
                pack_lot_line.set_lot_name(options.lot);
                line.pack_lot_lines.add(pack_lot_line);
            }
        }

        var to_merge_orderline;
        for (var i = 0; i < this.orderlines.length; i++) {
            if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
                to_merge_orderline = this.orderlines.at(i);
            }
        }
        if (to_merge_orderline){
            to_merge_orderline.merge(line);
        } else {
            this.orderlines.add(line);
        }
        this.select_orderline(this.get_last_orderline());

        if(line.has_product_lot && line.pack_lot_lines.length !== line.quantity){
            this.display_lot_popup();
        }
    },
})
});
