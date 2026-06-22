from odoo import fields, models


class ServicePackages(models.Model):
    _name = "service.packages"
    _description = "Vehicle Service Package"
    _inherit = ['mail.thread']
    

    name = fields.Char(
        string="Package Name",
        required=True
    )
    description = fields.Html(
        string="Description"
    )
    service_category_id = fields.Many2one(
        comodel_name = "service.category",
        string = "Service Category"
    )
    service_package_line_ids = fields.One2many(
        comodel_name = "package.service.line",
        inverse_name = "service_package_id",
    )