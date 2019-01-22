# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from odoo.addons.account.models import account_payment


account_payment.MAP_INVOICE_TYPE_PARTNER_TYPE.update({
        'out_paying': 'customer',
        'in_paying': 'supplier',

})

account_payment.MAP_INVOICE_TYPE_PAYMENT_SIGN.update({
    'out_paying': -1,
    'in_paying': 1,
})
MAP_INVOICE_TYPE_PARTNER_TYPE = account_payment.MAP_INVOICE_TYPE_PARTNER_TYPE
MAP_INVOICE_TYPE_PAYMENT_SIGN = account_payment.MAP_INVOICE_TYPE_PAYMENT_SIGN



class account_payment_method(models.Model):
    _inherit = "account.payment.method"
    _description = "Payment Methods"


