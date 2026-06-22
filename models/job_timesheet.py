from odoo import api, fields, models

class JobTimesheet(models.Model):

    _name = "job.timesheet"
    _description = "Job Timesheet Entry"
    _inherit = ['mail.thread']
    _rec_name = 'job_card_id'
    
    

    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )
    work_order_id = fields.Many2one(
        comodel_name = "work.orders",
        string = "Work order"
    )
    machanics_id = fields.Many2one(
        comodel_name="hr.employee",
        string = "Mechanic"
    )
    hours = fields.Float(
        string = "Hours"
    )
    labor_cost = fields.Float(
        string = "Labor Cost"
    )
   