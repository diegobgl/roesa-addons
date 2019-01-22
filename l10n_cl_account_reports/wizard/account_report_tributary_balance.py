# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models


class account_tributary_balance_report(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'tributary.balance.report'
    _description = 'Tributary Balance Report'


    journal_ids = fields.Many2many('account.journal', string='Journals', required=True)


    _defaults = {
        'journal_ids': [],
    }

    def _print_report(self, data):
        data = self.pre_print_report( data)
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].get_action(records, 'l10n_cl_account_reports.report_tributarybalance', data=data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
