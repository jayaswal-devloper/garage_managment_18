from odoo import api, fields, models


class FleetVehicleModel(models.Model):
	_inherit = "fleet.vehicle.model"
	_description = "Drivers history on a vehicle"
