# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Cubic ERP - Teradata SAC. (http://cubicerp.com).
#    Copyright (C) 2016 Blanco Martín & Asociados - Odoo Chile Community
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

class ResStateCity(models.Model):

    @api.multi
    def name_get(self):
        res = []
        for city in self:
            res.append((city.id, (city.code and '[' + city.code + '] ' or '') + city.name))
        return res

    _name = 'res.country.state.city'
    _description = u"City of state"
    
    name = fields.Char(u'City Name', size=256, required=True, help=u"The City Name",)
    code = fields.Char(u'City Code', size=32, required=True, help=u"The City code",)
    country_id = fields.Many2one('res.country', u'Country', required=True, help=u"",)
    state_id = fields.Many2one('res.country.state', u'State', 
        index=True, domain="[('country_id','=',country_id),('type','=','normal')]", help=u"",)
    type = fields.Selection([
        ('view',u'View'), 
        ('normal',u'Normal')], string=u'Type', default='normal', help=u"",)
    