from odoo import api, fields, models
from odoo.exceptions import ValidationError


class JobCardChecklistLine(models.Model):

    _name = 'job.card.checklist.line'
    _description ="Job Card Checklist Item"
    _inherit = ['mail.thread']


    name = fields.Char(
        string="Name"
    )
    sequence = fields.Integer(
        string="Sequence"
    )
    description = fields.Text(
        string="Description"
    )
    required = fields.Boolean(
        string="Required"
    )
    done = fields.Boolean(
        string = "Done"
    )
    note = fields.Text(
        string = "Note"
    )
    completed_by = fields.Many2one(
        comodel_name = "hr.employee",
        string = "Completed By"
    )
    completed_on = fields.Datetime(
        string = "Completed On"
    )
    checklist_tmpl_id = fields.Many2one(
        comodel_name = "service.checklist",
        string="Checklist Template",
        compute = "_compute_job_card_id"
    )
    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )


    @api.depends('job_card_id')
    def _compute_job_card_id(self):
        for rec in self:
            if rec.job_card_id:
                rec.checklist_tmpl_id = rec.job_card_id.service_checklist_id.id
            else:
                rec.checklist_tmpl_id = False


    # @api.constrains('required','done')
    # def _check_required_done(self):
    #     for rec in self:
    #         if rec.required and not rec.done:
    #             raise ValidationError(
    #                 f"'{rec.name}' is a required checklist item. Please complete it before marking the job card as completed."
    #             )