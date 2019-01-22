
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 ITS-1 (<http://www.its1.lv/>)
#                       E-mail: <info@its1.lv>
#                       Address: <Vienibas gatve 109 LV-1058 Riga Latvia>
#                       Phone: +371 66116534
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

class AccountTaxGroup(models.Model):
    _inherit = 'account.tax'


    processing = fields.Selection([('no_tax', 'Non taxable'),
                                       ('holding_tax', 'With holding tax')],
                                      string='Tax Processing')



class AccountAccountType(models.Model):
    _inherit = "account.account.type"
    _description = "Account Type"

    result_type = fields.Selection([
        ('asset', 'Asset'),
        ('liability','Liability'),
        ('equity', 'Equity'),
        ('result', 'Result'),
    ],
        help="The 'Result Type' is used for features available on "\
        "different types of accounts: asset, liability and equity type is for asset or liability accounts"\
        ", result type is for loss / profit accounts.", string="Result type")