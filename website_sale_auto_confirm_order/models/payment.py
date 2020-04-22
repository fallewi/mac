# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp import models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def form_feedback(self, data, acquirer_name):
        super().form_feedback(data, acquirer_name)

        tx = None
        # fetch the tx, check its state, confirm the potential SO
        tx_find_method_name = '_%s_form_get_tx_from_data' % acquirer_name
        if hasattr(self, tx_find_method_name):
            tx = getattr(self, tx_find_method_name)(data)
        if tx:
            tx.sale_order_id.action_confirm()

        return True
