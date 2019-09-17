odoo.define('pos_kitchen_screen.send_to_kitchen_screen', function (require) {
"use strict";
var screens = require('point_of_sale.screens');
var session = require('web.session');

var SendToKicthenButton = screens.ActionButtonWidget.extend({
    'template': 'pos_kitchen_screen.send_order_to_kitchen',
    button_click: function(){
        var order = this.pos.get_order();
        var changes = order.computeChanges();
        changes.session_id = this.pos.pos_session.id;
        if (changes.new.length || changes.cancel.length) {
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

});
