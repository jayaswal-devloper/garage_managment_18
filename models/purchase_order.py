from odoo import api, fields, models



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    job_card_id = fields.Many2one(
        'job.card',
        string='Job Card'
    )