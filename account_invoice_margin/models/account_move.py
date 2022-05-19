# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    margin = fields.Monetary(compute="_compute_margin", store=True)
    margin_signed = fields.Monetary(compute="_compute_margin", store=True)
    margin_percent = fields.Float(
        string="Margin (%)",
        digits="Product Price",
        compute="_compute_margin",
        store=True,
    )

    def _get_margin_applicable_lines(self):
        self.ensure_one()
        return self.invoice_line_ids

    @api.depends(
        "invoice_line_ids.margin",
        "invoice_line_ids.margin_signed",
        "invoice_line_ids.price_subtotal",
    )
    def _compute_margin(self):
        for invoice in self:
            margin = 0.0
            margin_signed = 0.0
            price_subtotal = 0.0
            for line in invoice._get_margin_applicable_lines():
                margin += line.margin
                margin_signed += line.margin_signed
                price_subtotal += line.price_subtotal
            invoice.margin = margin
            invoice.margin_signed = margin_signed
            invoice.margin_percent = (
                price_subtotal and margin_signed / price_subtotal * 100 or 0.0
            )
