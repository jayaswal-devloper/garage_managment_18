from odoo import api, models ,fields

class VehicalWorkshop(models.Model):
    _name = "vehical.workshop"
    _description = "Vehical workshop"
    _inherit = ['mail.thread']
    

    name = fields.Char(
        string='Workshop Name'
    )
    code = fields.Char(
        string="Code"
    )
    address = fields.Char(
        string="Address"
    )
    phone = fields.Char(
        string="Phone"
    )
    email = fields.Char(
        string="Email"
    )
    Workshop_manager_id = fields.Many2one(
        comodel_name="hr.employee",
        string = "Workshop Manager"
    )
    machanics_ids = fields.Many2many(
        comodel_name = "hr.employee",
        string = 'Machanics'
    )
    active = fields.Boolean(
        string="Active"
    )