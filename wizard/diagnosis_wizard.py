from odoo import models, fields, api

class DiagnosisWizard(models.TransientModel):
    _name = "diagnosis.wizard"
    _description = "Diagnosis Wizard" 

    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )
    diagnosis_detail = fields.Text(
        string="Diagnosis Details"
    )
    machanics_id = fields.Many2one(
        comodel_name = "hr.employee",
        string = "Mechanic"
    )
    job_card_service_charge_line_ids = fields.One2many(
        related='job_card_id.job_card_service_charge_line_ids',
        readonly=False,
    )
    job_card_vehicle_part_ids = fields.One2many(
        related='job_card_id.spare_parts_ids',
        readonly=False,
    )


    def action_confirm(self):
        for wizard in self:

            diagnosis = self.env['vehicle.diagnosis'].search([
                ('job_card_id', '=', wizard.job_card_id.id)
            ], limit=1)

            vals = {
                'job_card_id': wizard.job_card_id.id,
                'diagnosis_detail': wizard.diagnosis_detail,
                'machanics_id': wizard.machanics_id.id,
                'job_card_service_charge_line_ids':[
                        (6, 0, wizard.job_card_service_charge_line_ids.ids)
                ],
                'job_card_vehicle_part_ids':[
                        (6,0,wizard.job_card_vehicle_part_ids.ids)
                ]
            }

            if diagnosis:
                diagnosis.write(vals)
            else:
                self.env['vehicle.diagnosis'].create(vals)

        return {
            'type': 'ir.actions.act_window_close',
        }