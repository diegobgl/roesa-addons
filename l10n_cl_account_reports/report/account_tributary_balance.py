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

import time
from odoo import api, models


class account_tributary_balance(models.AbstractModel):
    _name = 'report.l10n_cl_account_reports.report_tributarybalance'

    sum_debit = 0.00
    sum_credit = 0.00
    sum_debitor = 0.00
    sum_creditor = 0.00
    sum_asset = 0.00
    sum_liability = 0.00
    sum_loss = 0.00
    sum_profit = 0.00
    # self.debit = self.credit = self.debitor = self.creditor = self.asset = self.liability = self.loss = self.profit = 0.00  #

    '''    def __init__(self, *args, **kwargs):
            super(account_tributary_balance, self).__init__(args,kwargs)
            self.sum_debit = 0.00
            self.sum_credit = 0.00
            self.sum_debitor = 0.00
            self.sum_creditor = 0.00
            self.sum_asset = 0.00
            self.sum_liability = 0.00
            self.sum_loss = 0.00
            self.sum_profit = 0.00
            self.debit = self.credit = self.debitor = self.creditor = self.asset = self.liability = self.loss = self.profit = 0.00#
    '''

    #   self.date_lst = []
    #    self.date_lst_string = ''
    #    self.result_acc = []
    #    self.localcontext.update({
    #        'time': time,
    #        'lines': self.lines,
    #        'sum_debit': self._sum_debit,
    #        'sum_credit': self._sum_credit,
    #        'get_fiscalyear':self._get_fiscalyear,
    #        'get_filter': self._get_filter,
    #        'get_start_period': self.get_start_period,
    #        'get_end_period': self.get_end_period ,
    #        'get_account': self._get_account,
    #        'get_journal': self._get_journal,
    #        'get_start_date':self._get_start_date,
    #        'get_end_date':self._get_end_date,
    #        'get_target_move': self._get_target_move,
    #        'totals':self.totals,
    #    })


    # def set_context(self, objects, data, ids, report_type=None):
    #    new_ids = ids
    #    if (data['model'] == 'ir.ui.menu'):
    #        new_ids = 'chart_account_id' in data['form'] and [data['form']['chart_account_id']] or []
    #        objects = self.pool.get('account.account').browse(self.cr, self.uid, new_ids)
    #    return super(account_tributary_balance, self).set_context(objects, data, new_ids, report_type=report_type)

    def lines(self, form, ids=None, done=None):
        def suma_subtotal(res, account_rec):
            if res['type'] != 'view':
                self.sum_debitor += res['debitor']
                self.sum_creditor += res['creditor']
                self.sum_asset += res['asset']
                self.sum_liability += res['liability']
                self.sum_loss += res['loss']
                self.sum_profit += res['profit']

                self.sum_debit += account_rec['debit']
                self.sum_credit += account_rec['credit']

        def suma(res):

            for item in self.result_acc:
                if not res['parent_id']: continue

                if item['id'] == res['parent_id'][0]:

                    if item['debitor'] >= 0:
                        if res['type'] == 'view' and (res['debitor'] - item['debitor']) >= 0:
                            item['debitor'] += (res['debitor'] - item['debitor'])
                        else:
                            item['debitor'] += res['debitor']

                    if item['creditor'] >= 0:
                        if res['type'] == 'view' and (res['creditor'] - item['creditor']) >= 0:
                            item['creditor'] += (res['creditor'] - item['creditor'])
                        else:
                            item['creditor'] += res['creditor']

                    if item['asset'] >= 0:
                        if res['type'] == 'view' and (res['asset'] - item['asset']) >= 0:
                            item['asset'] += (res['asset'] - item['asset'])
                        else:
                            item['asset'] += res['asset']

                    if item['liability'] >= 0:
                        if res['type'] == 'view' and (res['liability'] - item['liability']) >= 0:
                            item['liability'] += (res['liability'] - item['liability'])
                        else:
                            item['liability'] += res['liability']

                    if item['loss'] >= 0:
                        if res['type'] == 'view' and (res['loss'] - item['loss']) >= 0:
                            item['loss'] += (res['loss'] - item['loss'])
                        else:
                            item['loss'] += res['loss']

                    if item['profit'] >= 0:
                        if res['type'] == 'view' and (res['profit'] - item['profit']) >= 0:
                            item['profit'] += (res['profit'] - item['profit'])
                        else:
                            item['profit'] += res['profit']

                    suma(item)

        def _process_child(accounts, disp_acc, parent):
            account_rec = [acct for acct in accounts if acct['id'] == parent][0]
            currency_obj = self.pool.get('res.currency')
            acc_id = self.pool.get('account.account').browse(self.cr, self.uid, account_rec['id'])
            currency = acc_id.currency_id and acc_id.currency_id or acc_id.company_id.currency_id
            res = {
                'id': account_rec['id'],
                'type': account_rec['type'],
                'code': account_rec['code'],
                'name': account_rec['name'],
                'level': account_rec['level'],
                'debit': account_rec['debit'],
                'credit': account_rec['credit'],
                'debitor': 0.00,
                'creditor': 0.00,
                'asset': 0.00,
                'liability': 0.00,
                'loss': 0.00,
                'profit': 0.00,
                'balance': account_rec['balance'],
                'parent_id': account_rec['parent_id'],
                'bal_type': '',
            }

            acc_type = obj_acc_type.browse(self.cr, self.uid, account_rec['user_type'][0])

            # deudor o acreedor
            if res['type'] != 'view':

                debit = account_rec['debit'] - account_rec['credit']
                if (debit > 0):
                    res['debitor'] = debit
                elif (debit < 0):
                    res['creditor'] = debit * -1

                # activo o pasivo
                if (acc_type.code in ['asset', 'bank', 'cash', 'receivable', 'liability', 'payable', 'equity']):
                    if res['debitor'] > 0:
                        res['asset'] = res['debitor']

                    if res['creditor'] > 0:
                        res['liability'] = res['creditor']

                # perdida o ganancia
                if (acc_type.code in ['expense', 'income']):
                    if res['debitor'] > 0:
                        res['loss'] = res['debitor']

                    if res['creditor'] > 0:
                        res['profit'] = res['creditor']


                        # self.sum_debit += account_rec['debit']
            # self.sum_credit += account_rec['credit']
            if disp_acc == 'movement':
                if not currency_obj.is_zero(self.cr, self.uid, currency, res['credit']) or not currency_obj.is_zero(
                        self.cr, self.uid, currency, res['debit']) or not currency_obj.is_zero(self.cr, self.uid,
                                                                                               currency,
                                                                                               res['balance']):
                    self.result_acc.append(res)
                    suma(res)
                    suma_subtotal(res, account_rec)
            elif disp_acc == 'not_zero':
                if not currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
                    self.result_acc.append(res)
                    suma(res)
                    suma_subtotal(res, account_rec)
            else:
                self.result_acc.append(res)
                suma(res)
                suma_subtotal(res, account_rec)

            if account_rec['child_id']:
                for child in account_rec['child_id']:
                    _process_child(accounts, disp_acc, child)

        obj_account = self.pool.get('account.account')
        obj_acc_type = self.pool.get('account.account.type')
        if not ids:
            ids = self.ids
        if not ids:
            return []
        if not done:
            done = {}

        ctx = self._context.copy()

        # ctx['fiscalyear'] = form['fiscalyear_id']
        if form['filter'] == 'filter_period':
            ctx['period_from'] = form['period_from']
            ctx['period_to'] = form['period_to']
        elif form['filter'] == 'filter_date':
            ctx['date_from'] = form['date_from']
            ctx['date_to'] = form['date_to']
        ctx['state'] = form['target_move']
        parents = ids
        child_ids = obj_account._get_children_and_consol(self.cr, self.uid, ids, ctx)
        if child_ids:
            ids = child_ids
        accounts = obj_account.read(self.cr, self.uid, ids,
                                    ['type', 'user_type', 'code', 'name', 'debit', 'credit', 'balance', 'parent_id',
                                     'level', 'child_id'], ctx)

        for parent in parents:
            if parent in done:
                continue
            done[parent] = 1
            _process_child(accounts, form['display_account'], parent)
        return self.result_acc

    def _get_accounts(self, accounts, display_account):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """

        def suma_subtotal(res):

            self.sum_debitor += res['debitor']
            self.sum_creditor += res['creditor']
            self.sum_asset += res['asset']
            self.sum_liability += res['liability']
            self.sum_loss += res['loss']
            self.sum_profit += res['profit']

            self.sum_debit += res['debit']
            self.sum_credit += res['credit']

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env['account.move.line']._query_get()
        tables = tables.replace('"', '')
        if not tables:
            tables = 'account_move_line'
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        # compute the balance, debit and credit for the provided accounts
        request = (
        "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
        " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(request, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in
                       ['type', 'credit', 'debit', 'balance', 'debitor', 'creditor', 'asset', 'liability', 'loss',
                        'profit'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id

            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result.keys():
                res['type'] = 'line'
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')

                # deudor o acreedor

                if (res['debit'] > res['credit']):
                    res['debitor'] = res['balance']
                elif (res['debit'] < res['credit']):
                    res['creditor'] = res['balance'] * -1

                # activo o pasivo
                act_pas = [a for a in account.tag_ids if a.name in ['activo', 'pasivo', 'patrimonio']]
                result = [a for a in account.tag_ids if a.name == 'resultado']
                if (account.user_type_id.result_type in ['asset', 'liability', 'equity']):
                    if account.user_type_id.result_type == 'asset':
                        res['asset'] = res['balance']

                    if account.user_type_id.result_type in ['liability', 'equity']:
                        res['liability'] = res['balance']

                # perdida o ganancia
                if (account.user_type_id.result_type == 'result'):
                    if res['balance'] > 0:
                        res['profit'] = res['balance']

                    if res['balance'] < 0:
                        res['loss'] = res['balance'] * -1

            if display_account == 'all':
                account_res.append(res)
                suma_subtotal(res)
            if display_account in ['movement', 'not_zero'] and not currency.is_zero(res['balance']):
                account_res.append(res)
                suma_subtotal(res)

        return self.totals(account_res)

    def totals(self, account_res):
        balance_res = self.sum_credit - self.sum_debit
        saldos_res = self.sum_debitor - self.sum_creditor
        inventario_res = self.sum_asset - self.sum_liability
        resultado_res = self.sum_loss - self.sum_profit

        balance_res = balance_res * -1 if balance_res < 0 else balance_res
        saldos_res = saldos_res * -1 if saldos_res < 0 else saldos_res
        inventario_res = inventario_res * -1 if inventario_res < 0 else inventario_res
        resultado_res = resultado_res * -1 if resultado_res < 0 else resultado_res

        item = {'type': 'total',
                'name': 'Suma',
                'code': '',
                'credit': self.sum_credit,
                'debit': self.sum_debit,
                'debitor': self.sum_debitor,
                'creditor': self.sum_creditor,
                'asset': self.sum_asset,
                'liability': self.sum_liability,
                'loss': self.sum_loss,
                'profit': self.sum_profit,

                }

        res = [item]

        item = {'type': 'total',
                'name': 'Utilidad',
                'code': '',
                'credit': balance_res if self.sum_credit < self.sum_debit else 0,
                'debit': balance_res if self.sum_debit < self.sum_credit else 0,
                'debitor': saldos_res if self.sum_debitor < self.sum_creditor else 0,
                'creditor': saldos_res if self.sum_creditor < self.sum_debitor else 0,
                'asset': inventario_res if self.sum_asset < self.sum_liability else 0,
                'liability': inventario_res if self.sum_liability < self.sum_asset else 0,
                'loss': resultado_res if self.sum_loss < self.sum_profit else 0,
                'profit': resultado_res if self.sum_profit < self.sum_loss else 0,

                }

        res.append(item)

        item = {'type': 'total',
                'name': 'Totales',
                'code': '',
                'credit': self.sum_credit + balance_res if self.sum_credit < self.sum_debit else self.sum_credit,
                'debit': self.sum_debit + balance_res if self.sum_debit < self.sum_credit else self.sum_debit,
                'debitor': self.sum_debitor + saldos_res if self.sum_debitor < self.sum_creditor else self.sum_debitor,
                'creditor': self.sum_creditor + saldos_res if self.sum_creditor < self.sum_debitor else self.sum_creditor,
                'asset': self.sum_asset + inventario_res if self.sum_asset < self.sum_liability else self.sum_asset,
                'liability': self.sum_liability + inventario_res if self.sum_liability < self.sum_asset else self.sum_liability,
                'loss': self.sum_loss + resultado_res if self.sum_loss < self.sum_profit else self.sum_loss,
                'profit': self.sum_profit + resultado_res if self.sum_profit < self.sum_loss else self.sum_profit,

                }

        res.append(item)

        return account_res + res

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        accounts = docs if self.model == 'account.account' else self.env['account.account'].search([])
        account_res = self.with_context(data['form'].get('used_context'))._get_accounts(accounts, display_account)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
        }
        return self.env['report'].render('l10n_cl_account_reports.report_tributarybalance', docargs)

# class report_tributarybalance(osv.AbstractModel):
#    _name = 'report.l10n_cl_account_reports.report_tributarybalance'
#    #_inherit = 'report.abstract_report'
#    #_template = 'l10n_cl_account_reports.report_tributarybalance'
#    _wrapped_report_class = account_tributary_balance

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
