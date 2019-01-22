# -*- encoding: utf-8 -*-
from odoo import api, fields, models
import re


class res_partner(models.Model):

    _inherit = 'res.partner'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):

        ids = []
        if name:
            ptrn_name = re.compile('(\[(.*?)\])')
            res_name = ptrn_name.search(name)
            if res_name:
                name = name.replace('[' + res_name.group(2) + '] ', '')
            partner_search = super(res_partner, self).name_search(name, args, operator, limit)
            ids = [partner[0] for partner in partner_search]
            ids = self.search([('id','in',ids)])
            if not ids:
                ids = self.search([('vat', operator, name)] + args, limit=limit)

            #if not ids:
            #    ptrn = re.compile('(\[(.*?)\])')
            #    res = ptrn.search(name)
            #    if res:
            #        ids = self.search([('vat', operator, res.group(2))] + args, limit=limit)

        else:
            return super(res_partner, self).name_search(name, args, operator, limit)

        return ids.name_get()

    # TODO ver si lo borramos, decidimos no mostrarlo por ahora
    # def name_get(self, cr, uid, ids, context=None):
    #     if isinstance(ids, (list, tuple)) and not len(ids):
    #         return []
    #     if isinstance(ids, (long, int)):
    #         ids = [ids]
    #     res_name = super(res_partner, self).name_get(cr, uid, ids, context)
    #     res = []
    #     for record in res_name:
    #         partner = self.browse(cr, uid, record[0], context=context)
    #         name = record[1]
    #         if partner.vat:
    #             name = '[' + partner.vat + '] ' + name
    #         res.append((record[0], name))
    #     return res
