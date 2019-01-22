# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    number_change = fields.Char("number change")

    @api.multi
    def action_invoice_open(self):

        super(AccountInvoice, self).action_invoice_open()

        for inv in self:
            if inv.number_change:
                inv.move_id.name = inv.number = inv.number_change

            self._cr.execute(""" UPDATE account_move_line SET ref=%s
                           WHERE move_id=%s AND (ref IS NULL OR ref = '/')""",
                             (inv.number_change, inv.move_id.id))
            self._cr.execute(""" UPDATE account_analytic_line SET ref=%s
                           FROM account_move_line
                           WHERE account_move_line.move_id = %s AND
                                 account_analytic_line.move_id = account_move_line.id""",
                             (inv.number_change, inv.move_id.id))


