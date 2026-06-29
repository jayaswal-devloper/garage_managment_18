from odoo import api, fields, models

class JobCardServiceChargeLine(models.Model):
    _name = "job.card.service.charge.line"
    _description = "Job Card Service Charge Item"
    _inherit = ['mail.thread']
    _rec_name = "product_id"

    product_id = fields.Many2one(
        comodel_name = "product.template",
        string = "Product"
    )
    description = fields.Text(
        string="Description"
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        readonly=True,
        related='product_id.uom_id',
        store=True,
    )
    quantity = fields.Float(
        string = "Quantity",
    )
    unit_price = fields.Float(
        string = "Unit Price"
    )
    subtotal = fields.Float(
        string = "Subtotal",
        compute = "_compute_subtotal",
        store = True
    )
    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )
    diagnosis_id = fields.Many2one(
        comodel_name = "vehicle.diagnosis",
        string = "Diagnosis"
    )

    @api.depends('quantity','unit_price')
    def _compute_subtotal(self):
        for rec in self:
            if rec.quantity and rec.unit_price:
                rec.subtotal = rec.quantity * rec.unit_price
            else :
                rec.subtotal = 0.00

    @api.onchange('product_id', 'job_card_id')
    def _onchange_product_id(self):
        for rec in self:

            package_line = self.env['package.service.line'].search([
                ('service_package_id', '=', rec.job_card_id.package_id.id),
                ('product_id', '=', rec.product_id.id)
            ], limit=1)

            if package_line:
                rec.unit_price = package_line.list_price
                rec.uom_id = package_line.product_id.uom_id.id

            else:
                rec.unit_price = rec.product_id.list_price
                rec.uom_id = rec.product_id.uom_id.id
