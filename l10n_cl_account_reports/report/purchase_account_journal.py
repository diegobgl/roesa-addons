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
import locale
from openerp.osv import osv
from openerp.tools.translate import _
from openerp.report import report_sxw
locale.setlocale(locale.LC_ALL, "es_ES.utf-8")

class journal_invoice_print(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(journal_invoice_print, self).__init__(cr, uid, name, context=context)
        self.context = context
        self.period_ids = []
        self.last_move_id = False
        self.journal_ids = []
        self.sort_selection = 'am.name'
        self.buffer_lines = []
        self.localcontext.update({
            'time': time,
            'lines': self.lines,
            'sum_debit': self._sum_debit,
            'sum_credit': self._sum_credit,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_account': self._get_account,
            'get_filter': self._get_filter,
            'get_start_date': self._get_start_date,
            'get_end_date': self._get_end_date,
            'get_fiscalyear': self._get_fiscalyear,
            'display_currency':self._display_currency,
            'get_sortby': self._get_sortby,
            'get_target_move': self._get_target_move,
            'check_last_move_id': self.check_last_move_id,
            'set_last_move_id': self.set_last_move_id,
            'tax_codes': self.tax_codes,
            'sum_vat': self._sum_vat,
            'get_nontaxable':self._get_nontaxable,
            'get_withholdingtax':self._get_withholdingtax,
            'get_amount_total': self._get_amount_total,
            'get_amount_untaxed': self._get_amount_untaxed,
            'get_amount_tax': self._get_amount_tax,
            'sum_nontaxable':self._sum_nontaxable,
            'sum_amount_untaxed':self._sum_amount_untaxed,
            'sum_amount_tax':self._sum_amount_tax,
            'sum_withholdingtax':self._sum_withholdingtax,
            'sum_total':self._sum_total
            
    })

    def set_context(self, objects, data, ids, report_type=None):
        obj_move = self.pool.get('account.move.line')
        new_ids = ids
        self.query_get_clause = ''
        self.target_move = data['form'].get('target_move', 'all')
        if (data['model'] == 'ir.ui.menu'):
            self.period_ids = tuple(data['form']['periods'])
            self.journal_ids = tuple(data['form']['journal_ids'])
            new_ids = data['form'].get('active_ids', [])
            self.query_get_clause = 'AND '
            self.query_get_clause += obj_move._query_get(self.cr, self.uid, obj='l', context=data['form'].get('used_context', {}))
            self.sort_selection = data['form'].get('sort_selection', 'date')
            objects = self.pool.get('account.journal.period').browse(self.cr, self.uid, new_ids)
        elif new_ids:
            #in case of direct access from account.journal.period object, we need to set the journal_ids and periods_ids
            self.cr.execute('SELECT period_id, journal_id FROM account_journal_period WHERE id IN %s', (tuple(new_ids),))
            res = self.cr.fetchall()
            self.period_ids, self.journal_ids = zip(*res)
        return super(journal_invoice_print, self).set_context(objects, data, ids, report_type=report_type)

    def set_last_move_id(self, move_id):
        self.last_move_id = move_id

    def check_last_move_id(self, move_id):
        '''
        return True if we need to draw a gray line above this line, used to separate moves
        '''
        if self.last_move_id:
            return not(self.last_move_id == move_id)
        return False

    def tax_codes(self, period_id, journal_id):
        ids_journal_period = self.pool.get('account.journal.period').search(self.cr, self.uid, 
            [('journal_id', '=', journal_id), ('period_id', '=', period_id)])
        self.cr.execute(
            'select distinct tax_code_id from account_move_line ' \
            'where period_id=%s and journal_id=%s and tax_code_id is not null and state<>\'draft\'',
            (period_id, journal_id)
        )
        ids = map(lambda x: x[0], self.cr.fetchall())
        tax_code_ids = []
        if ids:
            self.cr.execute('select id from account_tax_code where id in %s order by code', (tuple(ids),))
            tax_code_ids = map(lambda x: x[0], self.cr.fetchall())
        tax_codes = self.pool.get('account.tax.code').browse(self.cr, self.uid, tax_code_ids)
        return tax_codes

    def _sum_vat(self, period_id, journal_id, tax_code_id):
        self.cr.execute('select sum(tax_amount) from account_move_line where ' \
                        'period_id=%s and journal_id=%s and tax_code_id=%s and state<>\'draft\'',
                        (period_id, journal_id, tax_code_id))
        return self.cr.fetchone()[0] or 0.0

    def _sum_debit(self, period_id=False, journal_id=False):
        if journal_id and isinstance(journal_id, int):
            journal_id = [journal_id]
        if period_id and isinstance(period_id, int):
            period_id = [period_id]
        if not journal_id:
            journal_id = self.journal_ids
        if not period_id:
            period_id = self.period_ids
        if not (period_id and journal_id):
            return 0.0
        move_state = ['draft','posted']
        if self.target_move == 'posted':
            move_state = ['posted']

        self.cr.execute('SELECT SUM(debit) FROM account_move_line l, account_move am '
                        'WHERE l.move_id=am.id AND am.state IN %s AND l.period_id IN %s AND l.journal_id IN %s ' + self.query_get_clause + ' ',
                        (tuple(move_state), tuple(period_id), tuple(journal_id)))
        return self.cr.fetchone()[0] or 0.0

    def _sum_credit(self, period_id=False, journal_id=False):
        if journal_id and isinstance(journal_id, int):
            journal_id = [journal_id]
        if period_id and isinstance(period_id, int):
            period_id = [period_id]
        if not journal_id:
            journal_id = self.journal_ids
        if not period_id:
            period_id = self.period_ids
        if not (period_id and journal_id):
            return 0.0
        move_state = ['draft','posted']
        if self.target_move == 'posted':
            move_state = ['posted']

        self.cr.execute('SELECT SUM(l.credit) FROM account_move_line l, account_move am '
                        'WHERE l.move_id=am.id AND am.state IN %s AND l.period_id IN %s AND l.journal_id IN %s '+ self.query_get_clause+'',
                        (tuple(move_state), tuple(period_id), tuple(journal_id)))
        return self.cr.fetchone()[0] or 0.0

    def lines(self, period_id, journal_id=False):
        if not journal_id:
            journal_id = self.journal_ids
        else:
            journal_id = [journal_id]
        obj_mline = self.pool.get('account.move.line')
        obj_ainvoice = self.pool.get('account.invoice')
        
        self.cr.execute('update account_journal_period set state=%s where journal_id IN %s and period_id=%s and state=%s', ('printed', self.journal_ids, period_id, 'draft'))
        self.pool.get('account.journal.period').invalidate_cache(self.cr, self.uid, ['state'], context=self.context)

        move_state = ['draft','posted']
        if self.target_move == 'posted':
            move_state = ['posted']

        fg = self.pool.get('account.print.journal').fields_get(
            self.cr, self.uid, ['sort_selection'])
        allowed = [v for v, l in fg['sort_selection']['selection']]

        assert self.sort_selection in allowed, \
            "unknown sorting directive %s expected one of %s" % (
                self.sort_selection, allowed)

        res = []
        self.cr.execute('SELECT am.id FROM account_move_line l, account_move am WHERE l.move_id=am.id AND am.state IN %s AND l.period_id=%s AND l.journal_id IN %s ' + self.query_get_clause + ' ORDER BY '+ self.sort_selection + ', l.move_id',(tuple(move_state), period_id, tuple(journal_id) ))
        ids = [x[0] for x in  self.cr.fetchall()]
        ids = obj_ainvoice.search(self.cr, self.uid,[('move_id','in',ids)])
        for invoice in obj_ainvoice.browse(self.cr, self.uid, ids):        
            
            res += [{
                    'numero': invoice.number <> '/' and invoice.number or ('*'+str(invoice.move_id.id)),
                    'fecha': invoice.date_invoice,
                    'cliente': invoice.partner_id and invoice.partner_id.name[:23],
                    'rut': invoice.partner_id.vat and invoice.partner_id.vat[:23] if invoice.partner_id else '',
                    'exento':self._get_nontaxable(invoice),
                    'neto': self._get_amount_untaxed(invoice),#invoice.amount_untaxed,
                    'iva': self._get_amount_tax(invoice),#invoice.amount_tax,
                    'iva_retenido': self._get_withholdingtax(invoice),
                    'total': self._get_amount_total(invoice), 
                    'monto_moneda':invoice.amount_currency if 'amount_currency' in invoice._columns else 0  
                    }]
            
        self.buffer_lines = res
        return res


    def _set_get_account_currency_code(self, account_id):
        self.cr.execute("SELECT c.symbol AS code "\
                "FROM res_currency c,account_account AS ac "\
                "WHERE ac.id = %s AND ac.currency_id = c.id" % (account_id))
        result = self.cr.fetchone()
        if result:
            self.account_currency = result[0]
        else:
            self.account_currency = False

    def _get_fiscalyear(self, data):
        if data['model'] == 'account.journal.period':
            return self.pool.get('account.journal.period').browse(self.cr, self.uid, data['id']).fiscalyear_id.name
        return super(journal_invoice_print, self)._get_fiscalyear(data)

    def _get_account(self, data):
        if data['model'] == 'account.journal.period':
            return self.pool.get('account.journal.period').browse(self.cr, self.uid, data['id']).company_id.name
        return super(journal_invoice_print, self)._get_account(data)

    def _display_currency(self, data):
        if data['model'] == 'account.journal.period':
            return True
        return data['form']['amount_currency']

    def _get_sortby(self, data):
        # TODO: deprecated, to remove in trunk
        if self.sort_selection == 'date':
            return self._translate('Date')
        elif self.sort_selection == 'ref':
            return self._translate('Reference Number')
        return self._translate('Date')
    
    def _get_nontaxable(self, data):
        res = 0
        tax_line = data.tax_line
        for tax_line in data.tax_line:
            tax_code = tax_line.tax_code_id
            if tax_code.nontaxable:
                res += tax_line.base_amount
        return res
    
    def _get_withholdingtax(self, data):
        res = 0
        tax_line = data.tax_line
        for tax_line in data.tax_line:
            tax_code = tax_line.tax_code_id
            if tax_code.withholdingtax:
                res += tax_line.amount
        
        return res

    def _get_amount_total(self, data):
        res = 0
        res = data.amount_total
        if data.type =='in_paying':
            res = 0
            for line in data.invoice_line:
                if line.price_subtotal<0:
                    res += (line.price_subtotal*-1) 
        if data.type =='out_paying':
            res = 0
            for line in data.invoice_line:
                if line.price_subtotal>0:
                    res += (line.price_subtotal)                 

        
        return res + self._get_amount_tax(data)
    
    def _get_amount_tax(self, data):
        res = 0
        res = data.amount_tax
        if data.type =='in_paying':
            res = 0
            account_tax_obj = self.pool.get('account.tax')
            taxes = []
            for line in data.invoice_line:
                if line.price_subtotal<0:
                    for t in line.invoice_line_tax_id:
                        if t.company_id.id == data.company_id.id:
                            taxes.append(t)
                    computed_taxes = account_tax_obj.compute_all(self.cr, self.uid, taxes, line.price_unit * (100.0-line.discount) / 100.0, line.quantity)['taxes']

                    res += computed_taxes[0]['amount']*-1
            
        if data.type =='out_paying':
            res = 0
            account_tax_obj = self.pool.get('account.tax')
            taxes = []
            for line in data.invoice_line:
                if line.price_subtotal>0:
                    for t in line.invoice_line_tax_id:
                        if t.company_id.id == data.company_id.id:
                            taxes.append(t)
                    computed_taxes = account_tax_obj.compute_all(self.cr, self.uid, taxes, line.price_unit * (100.0-line.discount) / 100.0, line.quantity)['taxes']

                    res += computed_taxes[0]['amount']
        
        
        return res

    def _get_amount_untaxed(self, data):
        res = 0
        res = data.amount_untaxed
        
        if data.type =='in_paying':
            res = 0
            for line in data.invoice_line:
                if line.price_subtotal<0:
                    res += line.price_subtotal*-1
        
        if data.type =='out_paying':
            res = 0
            for line in data.invoice_line:
                if line.price_subtotal>0:
                    res += line.price_subtotal
        
        return res
    
    def _sum_amount_untaxed(self):
        
        res = 0
        for line in self.buffer_lines:
            res += line['neto']
            
        return res
        
        
    def _sum_amount_tax(self):
        
        res = 0
        for line in self.buffer_lines:
            res += line['iva']
            
        return res
    def _sum_nontaxable(self):
        
        res = 0
        for line in self.buffer_lines:
            res += line['exento']
            
        return res
    def _sum_withholdingtax(self):
        
        res = 0
        for line in self.buffer_lines:
            res += line['iva_retenido']
            
        return res
    
    def _sum_total(self):
        
        res = 0
        for line in self.buffer_lines:
            res += line['total']
            
        return res
        

    def _get_start_date(self, data):
        if data.get('form', False) and data['form'].get('date_from', False):
            return data['form']['date_from']
        return ''

    def _get_target_move(self, data):
        if data.get('form', False) and data['form'].get('target_move', False):
            if data['form']['target_move'] == 'all':
                return _('All Entries')
            return _('All Posted Entries')
        return ''

    def _get_end_date(self, data):
        if data.get('form', False) and data['form'].get('date_to', False):
            return data['form']['date_to']
        return ''

    def get_start_period(self, data):
        if data.get('form', False) and data['form'].get('period_from', False):
            return self.pool.get('account.period').browse(self.cr,self.uid,data['form']['period_from']).name
        return ''

    def get_end_period(self, data):
        if data.get('form', False) and data['form'].get('period_to', False):
            return self.pool.get('account.period').browse(self.cr, self.uid, data['form']['period_to']).name
        return ''

    def _get_filter(self, data):
        if data.get('form', False) and data['form'].get('filter', False):
            if data['form']['filter'] == 'filter_date':
                return self._translate('Date')
            elif data['form']['filter'] == 'filter_period':
                return self._translate('Periods')
        return self._translate('No Filters')

    def _sum_debit_period(self, period_id, journal_id=None):
        journals = journal_id or self.journal_ids
        if not journals:
            return 0.0
        self.cr.execute('SELECT SUM(debit) FROM account_move_line l '
                        'WHERE period_id=%s AND journal_id IN %s '+ self.query_get_clause +'',
                        (period_id, tuple(journals)))

        return self.cr.fetchone()[0] or 0.0

    def _sum_credit_period(self, period_id, journal_id=None):
        journals = journal_id or self.journal_ids
        if not journals:
            return 0.0
        self.cr.execute('SELECT SUM(credit) FROM account_move_line l '
                        'WHERE period_id=%s AND journal_id IN %s ' + self.query_get_clause +' ',
                        (period_id, tuple(journals)))
        return self.cr.fetchone()[0] or 0.0


    def _get_company(self, data):
        if data.get('form', False) and data['form'].get('chart_account_id', False):
            return self.pool.get('account.account').browse(self.cr, self.uid, data['form']['chart_account_id']).company_id.name
        return ''

    def _get_journal(self, data):
        codes = []
        if data.get('form', False) and data['form'].get('journal_ids', False):
            self.cr.execute('select code from account_journal where id IN %s',(tuple(data['form']['journal_ids']),))
            codes = [x for x, in self.cr.fetchall()]
        return codes

    def _get_currency(self, data):
        if data.get('form', False) and data['form'].get('chart_account_id', False):
            return self.pool.get('account.account').browse(self.cr, self.uid, data['form']['chart_account_id']).company_id.currency_id.symbol
        return ''    
    

class report_purchasejournal(osv.AbstractModel):
    _name = 'report.l10n_cl_account_reports.report_purchasejournal'
    _inherit = 'report.abstract_report'
    _template = 'l10n_cl_account_reports.report_purchasejournal'
    _wrapped_report_class = journal_invoice_print

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
