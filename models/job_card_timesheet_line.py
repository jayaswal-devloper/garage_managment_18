from odoo import api, fields, models

class JobCardTimesheetLine(models.Model):
    _name = 'job.card.timesheet.line'
    _description = 'Job Card Timesheet Line'
    _inherit = ['mail.thread']
    _rec_name = 'job_card_id'

    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )
    work_order_id = fields.Many2one(
        comodel_name = "work.orders",
        string = "Work Order"
    )
    machanics_id = fields.Many2one(
        comodel_name="hr.employee",
        string = "Mechanic"
    )  
    start_time = fields.Datetime(
        string = "Start Time"
    )
    end_time = fields.Datetime(
        string = "End Time"
    )
    hours = fields.Float(
        string = "Hours",
        compute="_compute_hours",
        store = True
    )
    labor_cost = fields.Float(
        string = "Labor Cost"
    )



  
    @api.depends("start_time", "end_time")
    def _compute_hours(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                diff = rec.end_time - rec.start_time
                rec.hours = diff.total_seconds() / 3600
            else:
                rec.hours = 0.0