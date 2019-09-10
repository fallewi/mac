odoo.define('pos_kitchen_screen.kitchen_screen', function (require) {
"use strict";

require('web.dom_ready');
var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
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
        this.render();
    },
    render: function(){
        this.$wrapper.html(qweb.render(this.template));
    },
});

});
