from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    job_card_id = fields.Many2one(
        'job.card',
        string='Job Card'
    )