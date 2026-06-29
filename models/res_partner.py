from odoo import api, fields, models

class Contact(models.Model):
	_inherit = "res.partner"
	_description = "Vehicle Owner"


	vehicle_ids = fields.One2many(
		comodel_name = "vehicle.detail",
		inverse_name = "partner_id",
	)