from odoo import api, fields, models



class GarageVehicleModel(models.Model):

    _name = "garage.vehicle.model"
    _description = "Vehicle Model"

    make_id = fields.Many2one(
        comodel_name = "garage.vehicle.make",
        string = "Vehicle Make"
    ) 
    name = fields.Char(
        string = "Model Name"
    )
    vehicle_type = fields.Selection(
        [('car', 'Car'), ('bike', 'Bike')], 
        string="Vehicle Type",
        default='car',
        required=True,
    )
    category_id = fields.Many2one(
      comodel_name = "vehicle.category",
      string = "Category"
    )
    fuel_type = fields.Selection([
            ('petrol', 'Petrol'),
            ('gasoline', 'Gasoline'),
            ('diesel', 'Diesel'),
            ('electric', 'Electric'),
            ('ev', 'EV'),
            ('hybrid', 'Hybrid'),
            ('full_hybrid', 'Full Hybrid'),
            ('mild_hybrid', 'Mild Hybrid'),
            ('strong_hybrid', 'Strong Hybrid'),
            ('plug_in_hybrid', 'Plug-in Hybrid'),
            ('plug_in_hybrid_petrol', 'Plug-in Hybrid Petrol'),
            ('plug_in_hybrid_diesel', 'Plug-in Hybrid Diesel'),
            ('cng', 'CNG'),
        ],
        string = "Fuel Type"
    )
    transmission = fields.Selection([
            ('manual', 'Manual'),
            ('automatic', 'Automatic')
        ],
        string = 'Transmission'
    )


