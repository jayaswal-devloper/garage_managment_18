from odoo import api, fields, models

class ChecklistLine(models.Model):

    _name = 'garage.checklist.line'
    _description ="Vehicle Service Checklist Item"
    _inherit = ['mail.thread']


    name = fields.Char(
        string="Item"
    )
    checklist_id = fields.Many2one(
        comodel_name='service.checklist',
        string="Checklist"
    )
    sequence = fields.Integer(
        string="Sequence"
    )
    description = fields.Char(
        string="Description"
    )
    required = fields.Boolean(
        string="Required"
    )