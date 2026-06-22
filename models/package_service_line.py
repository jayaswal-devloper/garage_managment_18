from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PackageServiceLine(models.Model):
    _name = "package.service.line"
    _description ="Job Card Service Charge"
    _inherit = ['mail.thread']
    _rec_name = 'product_id'
    


    product_id = fields.Many2one(
        comodel_name = "product.template",
        string = "Service"
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure',
        readonly=True,
        related='product_id.uom_id',
        store=True,
    )
    service_package_id = fields.Many2one(
        comodel_name = "service.packages",
        string = "Package"
    ) 
    free_of_charge = fields.Boolean(
        string = "Free Of charge"
    )
    discount = fields.Float(
        string = "Discount(%)"
    )
    list_price = fields.Float(
        string = "Sales Price"
    )

    @api.constrains('discount')
    def _check_discount(self):
        for rec in self:
            if rec.discount > 100:
                raise ValidationError(
                    "You cannot enter a discount greater than 100%."
                )


    @api.onchange('product_id','free_of_charge','discount')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id and rec.free_of_charge == False:
                rec.list_price = rec.product_id.list_price
                if rec.list_price and rec.discount:
                    rec.list_price = rec.list_price - (rec.list_price*rec.discount)/100
            elif rec.product_id and rec.free_of_charge == True:
                rec.list_price = 0.00
                rec.discount = 100