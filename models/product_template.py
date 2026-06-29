from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description="Vehical Service package"


    is_service_package = fields.Boolean(
        string = "Service Package"
    )
    duration = fields.Integer(
        string = "Duration"
    )
    

    
    @api.onchange('is_service_package')
    def _onchange_is_service_package(self):
        if self.is_service_package == True:
            self.sale_ok = True
            self.purchase_ok = False
            self.type = 'service'