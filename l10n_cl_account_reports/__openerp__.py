# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-Today OpenERP S.A. (<http://www.openerp.com>).
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

{
    'name': 'Documentos Tributarios - Chile',
    'version': '1.0',
    'category': 'Localization/Chile',
    "description": """
    
    Agrega:
        Reportes Tributarios
=============================================================================
    """,
    'author':  'Pedro Arroyo M',
    'website': 'http://www.tierranube.cl',
    'depends': ['account'],
    'data': [
             'wizard/account_report_tributary_balance_view.xml',
             'views/report_tributarybalance.xml',
             #'wizard/account_report_print_journal_view.xml',
             #'views/report_salepurchasejournal.xml',
             #'views/report_salejournal.xml',
             #'views/report_purchasejournal.xml',
             'views/account_tax_code.xml',
             'account_report.xml',
            'data/account.account.tag.csv',
    ],
    'installable': True,
    'active': False,
}
