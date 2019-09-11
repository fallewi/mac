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
        this._super();
        this.$wrapper = $wrapper;
        this.orders = {};
        this.session_id = parseInt(this.$wrapper.data('session_id'));
        this.fetch_orders_url = '/kitchen/orders/' + this.session_id;
        console.log(this);
        this.fetch_orders();
    },
    render: function(){
        // TODO make a function with the callback
        var self = this;
        self.$wrapper.html(qweb.render(self.template, self.orders));
        self.$wrapper.off('click', '.js-next-step');
        this.$wrapper.on('click', '.js-next-step', function(event){
            var url = '/kitchen/order_next_step/' + parseInt($(event.target).data('order_id'));
            session.rpc(url).then(function(result){
                if(result.success) {
                    self.fetch_orders();
                }
            });
        });
    },
    fetch_orders: function(){
        var self = this;
        session.rpc(self.fetch_orders_url).then(function(result){
            // TODO: check if sometimes the same
            if(self.orders != result.data) {
                self.orders = result.data;
                self.render();
            }
        });
    },
});
    return KitchenScreen;
});
