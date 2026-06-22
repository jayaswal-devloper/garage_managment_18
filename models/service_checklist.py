from odoo import api, fields, models

class ServiceChecklist(models.Model):

    _name = "service.checklist"
    _description = "Service Inspection Checklist"
    _inherit = ['mail.thread']

    
    name = fields.Char(
        string="Name"
    )
    active = fields.Boolean(
        string="Active"
    )
    checklist_itme_ids = fields.One2many(
        comodel_name='garage.checklist.line',
        inverse_name="checklist_id",
        string = "Itmes"
    )