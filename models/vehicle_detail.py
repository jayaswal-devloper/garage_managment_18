from odoo import api, fields, models

class VehicleDetail(models.Model):
    _name = "vehicle.detail"
    _description = "Vehical Detail"

    #vehical detail
    name = fields.Char(
        string = "License Plate"
    )
    image_128 = fields.Image(
        related='mack_id.image_128',
        readonly=True
    )
    model_id = fields.Many2one(
        comodel_name = "garage.vehicle.model",
        string = "Model Name"
    )
    mack_id = fields.Many2one(
        comodel_name = "garage.vehicle.make",
        string = "Brand",
        related = "model_id.make_id",
        store = True
    )
    vehicle_type = fields.Selection(
        related="model_id.vehicle_type",
        string="Vehicle Type",
        store=True,
    )
    model_year = fields.Integer(
        string = "Model Year"
    )
    varient = fields.Char(
        string = "Varinet"
    )
    fuel_type = fields.Selection(
        related = "model_id.fuel_type",
        string = "Fuel Type"
    )
    transmission = fields.Selection(
        related = "model_id.transmission",
        string = 'Transmission'
    )
    color = fields.Char(
        string = "Color"
    )
    odometer = fields.Float(
        string = "Last Odometer"
    )

    #customer detail
    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        string = "Driver Name"
    )
    mobile_number = fields.Char(
        string = "Mobile Number"
    )
    email = fields.Char(
        string = "Email"
    )
    address = fields.Text(
        string = "Address"
    )


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.phone or self.partner_id.email:
                self.mobile_number = self.partner_id.phone
                self.email = self.partner_id.email
            elif self.partner_id.mobile or self.partner_id.email :
                self.mobile_number = self.partner_id.phone
                self.email = self.partner_id.email
            else :
                self.mobile_number = ''
                self.email = ''
               
