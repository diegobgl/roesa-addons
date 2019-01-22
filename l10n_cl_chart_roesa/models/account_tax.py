# -*- coding: utf-8 -*-

from odoo import models, api, fields, tools
import odoo.addons.decimal_precision as dp
from odoo.tools.translate import _

class AccountTaxTemplate(models.Model):

    _inherit = 'account.tax.template'
    
    sii_code = fields.Integer('SII Code')
    activo_fijo = fields.Boolean(string="Activo Fijo", default=False)
    
    def _get_tax_vals(self, company):
        vals = super(AccountTaxTemplate, self)._get_tax_vals(company)
        vals['sii_code'] = self.sii_code
        vals['activo_fijo'] = self.activo_fijo
        return vals
    
class AccountTax(models.Model):

    _inherit = 'account.tax'
    
    sii_code = fields.Integer('SII Code')
    activo_fijo = fields.Boolean(string="Activo Fijo", default=False)