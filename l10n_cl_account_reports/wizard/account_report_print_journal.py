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
from lxml import etree


class InvoicePrintJournal(models.TransientModel):
    _inherit = "account.common.report"
    _name = 'invoice.print.journal'
    _description = 'Account Invoice Print Journal'

    sort_selection = fields.Selection([('l.date', 'Date'),
                                            ('am.name', 'Journal Entry Number'),],
                                            'Entries Sorted by', required=True),
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True)


    _defaults = {
        'sort_selection': 'am.name',
        'filter': 'filter_period',
        'journal_ids': False,
    }

    @api.multi
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        '''
        used to set the domain on 'journal_ids' field: we exclude or only propose the journals of type 
        sale/purchase (+refund) accordingly to the presence of the key 'sale_purchase_only' in the context.
        '''

        context = dict(self._context or {})

        res = super(InvoicePrintJournal, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])

        if context.get('sale_purchase_only'):
            domain ="[('type', 'in', ('sale','purchase','sale_refund','purchase_refund'))]"
        elif context.get('sale_only'):
            domain ="[('type', 'in', ('sale','sale_paying', 'purchase_paying', 'sale_refund'))]"
        elif context.get('purchase_only'):
            domain ="[('type', 'in', ('purchase','sale_paying', 'purchase_paying', 'purchase_refund'))]"
        else:
            domain ="[('type', 'not in', ('sale','purchase','sale_refund','purchase_refund'))]"
        nodes = doc.xpath("//field[@name='journal_ids']")
        for node in nodes:
            node.set('domain', domain)
        res['arch'] = etree.tostring(doc)
        return res

    @api.multi
    def _print_report(self, ids, data, context=None):
        context = dict(self._context or {})
        data = self.pre_print_report(ids, data)
        data['form'].update(self.read(ids, ['sort_selection'])[0])
        if context.get('sale_purchase_only'):
            return self.pool['report'].get_action([], 'l10n_cl_account_reports.report_salepurchasejournal', data=data)
        elif context.get('sale_only'):
            return self.pool['report'].get_action([], 'l10n_cl_account_reports.report_salejournal', data=data)
        elif context.get('purchase_only'):
            return self.pool['report'].get_action([], 'l10n_cl_account_reports.report_purchasejournal', data=data)

        else:
            return self.pool['report'].get_action([], 'account.report_journal', data=data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
