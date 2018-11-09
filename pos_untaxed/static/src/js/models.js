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
});
