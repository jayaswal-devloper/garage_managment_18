from odoo import api, fields, models

class JobCardVehicleSpareParts(models.Model):
    _name = "job.card.vehicle.spare.parts"
    _description = "Vehical Spare Parts"
    _inherit = ['mail.thread']
    _rec_name = "product_id"


    product_id = fields.Many2one(
        comodel_name = "product.template",
        string = "Product"
    )
    quantity = fields.Float(
        string = "Quantity"
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure',
        readonly=True,
        related='product_id.uom_id',
        store=True,
    )
    unit_price = fields.Float(
        related='product_id.list_price',
        string = "Unit Price"
    )
    subtotal = fields.Float(
        string = "Sub total"
    )
    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )
    diagnosis_id = fields.Many2one(
        comodel_name = "vehicle.diagnosis",
        string = "Diagnosis"
    )


    @api.onchange('quantity','unit_price')
    def _onchange_subtotal(self):
        for rec in self:
            if rec.quantity and rec.unit_price:
                rec.subtotal = rec.quantity * rec.unit_price
            else :
                rec.subtotal = 0.00