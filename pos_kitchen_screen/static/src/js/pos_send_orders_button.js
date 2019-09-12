odoo.define('pos_kitchen_screen.send_to_kitchen_screen', function (require) {
"use strict";
var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');
var mixins = require('web.mixins');
var Session = require('web.Session');
var qweb = core.qweb;



var SendToKicthenButton = screens.ActionButtonWidget.extend({
    'template': 'pos_kitchen_screen.send_order_to_kitchen',
    button_click: function(){
        var order = this.pos.get_order();
        console.log(order);
    },
});

screens.define_action_button({
    'name': 'send_to_kitchen_button',
    'widget': SendToKicthenButton,
    'condition': function() {
        return this.pos.config.enable_kitchen_screen;
    },
});

});
