# Copyright (C) 2020 ArkeUp SAS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, list_fields):
        res = super(SaleOrder, self).default_get(list_fields)
        if self.env.user.brand_ids:
            res.update({'brand_id': self.env.user.brand_ids[0].id, 'team_id': self.env.user.brand_ids[0].team_id.id})
        return res

    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        super(SaleOrder, self)._onchange_brand_id()
        for rec in self:
            vals = {}
            if rec.brand_id.team_id:
                vals.update({'team_id': rec.brand_id.team_id.id})
            if rec.brand_id.analytic_account_id:
                vals.update({'analytic_account_id': rec.brand_id.analytic_account_id.id})
            rec.update(vals)

    @api.onchange('user_id')
    def onchange_user_id(self):
        res = super(SaleOrder, self).onchange_user_id()
        if self.brand_id:
            self.update({'team_id': self.brand_id.team_id.id})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one(related='order_id.brand_id', readonly=True, store=True)

# RunbotBuild skip test