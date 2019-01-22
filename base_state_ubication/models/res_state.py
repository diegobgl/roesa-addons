# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
# Copyright (c) 2012 Cubic ERP - Teradata SAC. (http://cubicerp.com).
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from odoo import models, api, fields
import odoo.addons.decimal_precision as dp
from odoo.tools.translate import _

class ResState(models.Model):

    @api.multi
    def name_get(self):
        res = []
        for state in self:
            data = []
            acc = state
            while acc:
                data.insert(0, acc.name)
                acc = acc.parent_id
            data = ' / '.join(data)
            res.append((state.id, (state.code and '[' + state.code + '] ' or '') + data))
        return res

    _name = 'res.country.state'
    _inherit = 'res.country.state'
    
    code = fields.Char(u'State Code', size=32, required=True, help=u"The state code")
    parent_id = fields.Many2one('res.country.state', u'Parent State', 
        required=False, index=True, domain=[('type','=','view')], help=u"",)
    child_ids = fields.One2many('res.country.state', 'parent_id', u'Child States', required=False, help=u"",)
    type = fields.Selection([
        ('view',u'View'), 
        ('normal',u'Normal')], string=u'Type', index=True, default='normal', help=u"",)
