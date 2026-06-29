from odoo import api, fields, models

class WorkOrder(models.Model):
    _name = "work.orders"
    _description = "Workshop Work Order"
    _inherit = ['mail.thread']
    

    name = fields.Char(
        string = "Work Order Number",
        default="New",
        readonly=True,
        copy=False
    )
    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )
    machanics_id = fields.Many2one(
        comodel_name="hr.employee",
        string = "Assigned Mechanic"
    )
    state = fields.Selection(
      [('draft','Draft'),('in_progress','In Progress'),('finished','Finished')],
      default = 'draft',
    )
    start_time = fields.Datetime(
        string = "Start Time"
    )
    end_time = fields.Datetime(
        string = "End Time"
    )
    job_timesheet_line_ids = fields.One2many(
        comodel_name = "job.card.timesheet.line",
        inverse_name = "work_order_id"
    )


    @api.onchange('job_card_id')
    def _onchange_job_card_id(self):
        self.job_timesheet_line_ids = [(5,0,0)]

        if self.job_card_id:
            timesheet_lines = []

            for item in self.job_card_id.job_timesheet_ids:
                timesheet_lines.append((0,0,{
                    'machanics_id':item.machanics_id.id,
                    'start_time':item.start_time,
                    'end_time':item.end_time,
                    'hours':item.hours,
                    'labor_cost':item.labor_cost,
                    }))

            self.job_timesheet_line_ids = timesheet_lines


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'garage.work.order'
            )

        return super().create(vals)

    def starting_work(self):
        for rec in self:
            rec.state = 'in_progress'
            rec.start_time = fields.datetime.today()


    def ending_work(self):
        for rec in self:
            rec.state = 'finished'
            rec.end_time = fields.datetime.today()
            rec.job_card_id.vehical_repaird = True

    