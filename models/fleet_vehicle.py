from odoo import api, fields, models
	
	
class FleetVehicle(models.Model):
	_inherit = "fleet.vehicle"
	_description = "Vehical Details"



	customer_id =  fields.Many2one(
		comodel_name = "hr.employee",
		string = "Customer"
	)
	last_service = fields.Date(
		string = "Last Service Date"
	)
	next_service = fields.Date(
		string = "Next Service Date"
	)
	notes = fields.Text(
		string = "Garage Notes"
	)