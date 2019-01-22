# -*- coding: utf-8 -*-

from odoo import models, api, fields, tools
import odoo.addons.decimal_precision as dp
from odoo.tools.translate import _

class AccountChartTemplate(models.Model):

    _inherit = 'account.chart.template'
    
    @api.multi
    def generate_account(self, tax_template_ref, acc_template_ref, code_digits, company):
        """ This method for generating accounts from templates.

            :param tax_template_ref: Taxes templates reference for write taxes_id in account_account.
            :param acc_template_ref: dictionary with the mappping between the account templates and the real accounts.
            :param code_digits: number of digits got from wizard.multi.charts.accounts, this is use for account code.
            :param company_id: company_id selected from wizard.multi.charts.accounts.
            :returns: return acc_template_ref for reference purpose.
            :rtype: dict
        """
        self.ensure_one()
        account_tmpl_obj = self.env['account.account.template']
        acc_template = account_tmpl_obj.search([('nocreate', '!=', True), ('chart_template_id', '=', self.id)], order='id')
        for account_template in acc_template:
            tax_ids = []
            for tax in account_template.tax_ids:
                tax_ids.append(tax_template_ref[tax.id])

            code_main = account_template.code and len(account_template.code) or 0
            code_acc = account_template.code or ''
            if code_main > 0 and code_main <= code_digits:
                code_acc = str(code_acc) + (str('0'*(code_digits-code_main)))
            vals = {
                'name': account_template.name,
                'currency_id': account_template.currency_id and account_template.currency_id.id or False,
                'code': code_acc,
                'user_type_id': account_template.user_type_id and account_template.user_type_id.id or False,
                'reconcile': account_template.reconcile,
                'note': account_template.note,
                'tax_ids': [(6, 0, tax_ids)],
                'company_id': company.id,
                'tag_ids': [(6, 0, [t.id for t in account_template.tag_ids])],
                'cod_f22': account_template.cod_f22,
                'conc': account_template.conc,
                'cap': account_template.cap,
                'acf': account_template.acf,
                'doc': account_template.doc,
                'cges': account_template.cges,
                'aneg': account_template.aneg,
                'caja': account_template.caja,
            }
            new_account = self.create_record_with_xmlid(company, account_template, 'account.account', vals)
            acc_template_ref[account_template.id] = new_account
        return acc_template_ref