odoo.define('mac_custom.checkout', function (require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var concurrency = require('web.concurrency');
    var dp = new concurrency.DropPrevious();

    /* Handle interactive carrier choice + cart update */
    var $pay_button = $('#o_payment_form_pay');

    var _activatePayButton = function() {
        $pay_button.prop('disabled', false);
    }

    var _onPeriodShippingClick = function(ev) {
        $pay_button.prop('disabled', true);
        var period_id = $(ev.currentTarget).val();
        var values = {'period_shipping': period_id};
        dp.add(ajax.jsonRpc('/shop/update_shipping_info', 'call', values))
            .then(_activatePayButton);
    };

    var $periods = $("#period_shipping_div input[name='period_shipping']");
    $periods.click(_onPeriodShippingClick);
    if ($periods.length > 0) {
        $periods.filter(':checked').click();
    }

    var $dateShipping = $("#date_shipping_div input[name='date_shipping']");
    $dateShipping.on('change', function () {
        $pay_button.prop('disabled', true);
        var values = {'date_shipping': $dateShipping.val()};
        dp.add(ajax.jsonRpc('/shop/update_shipping_info', 'call', values))
            .then(_activatePayButton);
    });

    var $specialInstruction = $("#special_instruction_div textarea[name='special_instruction']");
    $specialInstruction.on('change', function () {
        $pay_button.prop('disabled', true);
        var values = {'special_instruction': $specialInstruction.val()};
        dp.add(ajax.jsonRpc('/shop/update_shipping_info', 'call', values))
            .then(_activatePayButton);
    });

});
