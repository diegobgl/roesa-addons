# -*- coding: utf-8 -*-

from odoo import models, api, fields, tools
from odoo.tools.translate import _

class AccountAccount(models.Model):

    _inherit = 'account.account'
    
    cod_f22 = fields.Char(u'Cod. F22', size=256, required=False, help=u"",)
    conc = fields.Char(u'Conc', size=256, required=False, help=u"",)
    cap = fields.Boolean(u'Cap?', readonly=False, help=u"",)
    acf = fields.Boolean(u'AcF?', readonly=False, help=u"",)
    doc = fields.Boolean(u'Doc?', readonly=False, help=u"",)
    cges = fields.Boolean(u'CGes?', readonly=False, help=u"",)
    aneg = fields.Boolean(u'ANeg?', readonly=False, help=u"",)
    caja = fields.Boolean(u'Caja?', readonly=False, help=u"",)
    