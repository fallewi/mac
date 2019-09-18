odoo.define('pos_kitchen_screen.send_to_kitchen_screen', function (require) {
"use strict";
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var session = require('web.session');
var multiprint = require('pos_restaurant.multiprint');

var SendToKicthenButton = screens.ActionButtonWidget.extend({
    'template': 'pos_kitchen_screen.send_order_to_kitchen',
    button_click: function(){
        var order = this.pos.get_order();
        var changes = order.computeChanges();
        changes.session_id = this.pos.pos_session.id;
        if (changes.new.length || changes.cancelled.length) {
            session.rpc('/kitchen/update_order', changes).then(function(result) {
                if(result.success){
                    order.saveChanges();
                }
            });
        }
    },
});

screens.define_action_button({
    'name': 'send_to_kitchen_button',
    'widget': SendToKicthenButton,
    'condition': function() {
        return this.pos.config.enable_kitchen_screen;
    },
});

var _super_orderline = models.Orderline.prototype;
models.Orderline = models.Orderline.extend({
    initialize: function() {
        _super_orderline.initialize.apply(this,arguments);
        if (!this.pos.config.enable_kitchen_screen) {
            return;
        }
        if (typeof this.mp_dirty === 'undefined') {
            // mp dirty is true if this orderline has changed
            // since the last kitchen print
            // it's left undefined if the orderline does not
            // need to be printed to a printer.

            this.mp_dirty = true;
        }
        if (!this.mp_skip) {
            // mp_skip is true if the cashier want this orderline
            // not to be sent to the kitchen
            this.mp_skip  = false;
        }
    },
    set_quantity: function(quantity) {
        if (this.pos.config.enable_kitchen_screen && quantity !== this.quantity) {
            this.mp_dirty = true;
        }
        _super_orderline.set_quantity.apply(this,arguments);
    },
});

models.Order = models.Order.extend({
    hasChangesToSendToKitchen: function(){
        var changes = this.computeChanges();
        if ( changes['new'].length > 0 || changes['cancelled'].length > 0){
            return true;
        }
        return false;
    },
});

screens.OrderWidget.include({
    render_orderline: function(orderline) {
        var node = this._super(orderline);
        if (this.pos.config.enable_kitchen_screen) {
            if (orderline.mp_skip) {
                node.classList.add('skip');
            } else if (orderline.mp_dirty) {
                node.classList.add('dirty');
            }
        }
        return node;
    },
    click_line: function(line, event) {
        if (!this.pos.config.enable_kitchen_screen) {
            this._super(line, event);
        } else if (this.pos.get_order().selected_orderline !== line) {
            this.mp_dbclk_time = (new Date()).getTime();
        } else if (!this.mp_dbclk_time) {
            this.mp_dbclk_time = (new Date()).getTime();
        } else if (this.mp_dbclk_time + 500 > (new Date()).getTime()) {
            line.set_skip(!line.mp_skip);
            this.mp_dbclk_time = 0;
        } else {
            this.mp_dbclk_time = (new Date()).getTime();
        }

        this._super(line, event);
    },
});

screens.OrderWidget.include({
    update_summary: function(){
        this._super();
        var changes = this.pos.get_order().hasChangesToSendToKitchen();
        console.log(changes);
        var skipped = changes ? false : this.pos.get_order().hasSkippedChanges();
        var buttons = this.getParent().action_buttons;

        if (buttons && buttons.send_to_kitchen_button) {
            buttons.send_to_kitchen_button.highlight(changes);
            buttons.send_to_kitchen_button.altlight(skipped);
        }
    },
});

});
