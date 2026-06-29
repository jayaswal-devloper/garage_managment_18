from odoo import api, fields, models

class ServicePackageHistory(models.Model):
	_name = "service.package.history"
	_description = "Service Package Hisotry"
	_rec_name = "partner_id"


	vehicle_id = fields.Many2one(
		comodel_name = "vehicle.detail",
		string = "Vehicle"
	)
	state = fields.Selection([
			('draft','Draft'),
			('active','Active'),
			('expired','Expired')
		],default = "draft"
	)
	package_id = fields.Many2one(
		comodel_name = "product.template",
		string = "Package Name",
		domain="[('is_service_package', '=', True)]"
	)
	start_date = fields.Date(
		string = "Start Date"
	)
	expired_date = fields.Date(
		string = "Expired Date"
	)
	partner_id = fields.Many2one(
		comodel_name = "res.partner",
		string = "Customer"
	)
	sale_order_id = fields.Many2one(
		comodel_name = "sale.order",
		string = "Sale Order No"
	)



	api.depends('start_date','expired_date')
	def cron_update_package_state(self):
		today = fields.date.today()
		print("\n\n\n\n  ",today)
		expired_records = self.search([
			('expired_date','<',today),
			('state','!=','expired')
			])
		expired_records.write({'state':'expired'})

		active_record = self.search([
			('start_date','<=',today),
			('expired_date','>=',today),
			('state','!=','active')
			])
		active_record.write({
			'state':'active'
			})