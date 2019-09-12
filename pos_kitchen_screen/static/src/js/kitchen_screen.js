odoo.define('pos_kitchen_screen.kitchen_screen', function (require) {
"use strict";

require('web.dom_ready');
var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
var session = require('web.session');
var qweb = core.qweb;

var $wrapper = $('.o_pos_kitchen_screen');

if(!$wrapper.length) {
    return $.Deferred().reject("DOM doesn't contain '.o_pos_kitchen_screen'");
}
ajax.loadXML('/pos_kitchen_screen/static/src/xml/kitchen_screen.xml', qweb).then(function() {
    new KitchenScreen($wrapper);
})

var KitchenScreen = Widget.extend({
    template: 'pos_kitchen_screen.screen',
    events : {},
    init: function ($wrapper) {
        var self = this;
        self._super();
        self.$wrapper = $wrapper;
        self.orders = {};
        self.session_id = parseInt(self.$wrapper.data('session_id'));
        self.fetch_orders_url = '/kitchen/orders/' + self.session_id;
        self.fetch_orders();
        // refresh screen every 10 seconds
        setInterval(function() {self.fetch_orders()}, 10000);
    },
    render: function(){
        var self = this;
        self.$wrapper.html(qweb.render(self.template, self.orders));
        self.$wrapper.off('click', '.js-next-step');
        self.$wrapper.on('click', '.js-next-step', function(event){
            self.next_step_button_listener(event);
        });
    },
    fetch_orders: function(){
        var self = this;
        session.rpc(self.fetch_orders_url).then(function(result){
            if(result.success) {
                // Only re render if the order data has changed
                if(JSON.stringify(self.orders.confirmed) != JSON.stringify(result.data.confirmed)
                   || JSON.stringify(self.orders.in_progress) != JSON.stringify(result.data.in_progress)
                   || JSON.stringify(self.orders.done) != JSON.stringify(result.data.done)) {
                    self.orders = result.data;
                    self.render();
                }
            }
        });
    },
    next_step_button_listener: function(event) {
        var self = this;
        self.$wrapper.off('click', '.js-next-step');
        var url = '/kitchen/order_next_step/' + parseInt($(event.target).data('order_id'));
        session.rpc(url).then(function(result){
            if(result.success) {
                self.fetch_orders();
            }
        });
    }
});
    return KitchenScreen;
});
