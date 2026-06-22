from odoo import api, fields, models

class ServiceType(models.Model):

    _name = "service.type"
    _description = "Vehicle Service Type"
    _inherit = ['mail.thread']


    name = fields.Char(
        string = "service Type"
    )
    service_category_id = fields.Many2one(
        comodel_name = "service.category",
        string = "Service Category"
    )