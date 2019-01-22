# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  BMyA SA  (http://blancomartin.cl)
#    All Rights Reserved.
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
    "name": """Base vat extension""",
    'version': '10.0.0.0.1',
    'category': 'Utilities',
    'sequence': 12,
    'author':  'Pedro Arroyo M',
    'website': 'http://www.tierranube.cl',
    'license': 'AGPL-3',
    'summary': '',
    'description': """

=============================================================================
""",


    'depends': [
        'web','base_vat',
    ],
    'data': [
        'views/templates.xml',
        'views/res_partner.xml',
        # 'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
