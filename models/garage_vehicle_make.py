from odoo import api, models, fields

class GarageVehicleMake(models.Model):
	_name = "garage.vehicle.make"
	_description = "Vehicle Brand Name."


	name = fields.Char(
		string = "Brand Name",
		required = "1"
	)
	image_128 = fields.Image(
		string = "Logo",
		max_width=128,
		max_height=128
	)



