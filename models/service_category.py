from odoo import api, fields, models

class ServiceCategory(models.Model):
    _name = "service.category"
    _description = "Categories Used to Organize Services"
    _inherit = ['mail.thread']


    name = fields.Char(
        string="Service Category",
        required = True
    )
    service_type_ids = fields.One2many(
        comodel_name = "service.type",
        inverse_name = "service_category_id",
        string = "Service Types"
    )
    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )
    checklist_id = fields.Many2one(
        comodel_name = "service.checklist",
        string = "Checklist Template"
    )
