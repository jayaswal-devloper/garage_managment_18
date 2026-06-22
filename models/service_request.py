from odoo import api, models, fields

class ServiceRequest(models.Model):
    _name = "service.request"
    _description="Car Service Request"
    _inherit = ['mail.thread']
    

    name = fields.Char(
        string="Request No",
        default="New",
        readonly=True,
        copy=False
    )
    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        string="Customer"
    )
    vehical_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehicle",
        required =True
    )
    workshop_id = fields.Many2one(
        comodel_name = "vehical.workshop",
        string="Workshop"
    )
    description = fields.Html(
        string="Description"
    )
    request_date = fields.Datetime(
        string="Request Date",
        default=fields.Datetime.now
    )
    package_id = fields.Many2one(
        comodel_name = "service.packages",
        string = "Service Package"
    )
    status = fields.Selection(
        [('new','New'),('confirmed','Confirmed'),('cancelled','Cancelled')],
        string="State", default='new'
    )
    job_card_count = fields.Integer(
        compute="_compute_job_card_count"
    )



    @api.model
    def create(self,vals_list):
        if vals_list.get('name','New') == 'New':
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'garage.service.request'
                )
            return super().create(vals_list)

    def _compute_job_card_count(self):
        for rec in self:
            rec.job_card_count = self.env['job.card'].search_count([
                ('service_id', '=', rec.id)
            ])

    def action_view_job_cards(self):
        return{
            'type':'ir.actions.act_window',
            'name': 'Job Cards',
            'res_model': 'job.card',
            'view_mode': 'list,form',
            'domain': [('service_id', '=', self.id)],
        }

    def action_request_confirm(self):
        for rec in self:
            rec.status = 'confirmed'
            if rec.name:
                existing_job_card = self.env['job.card'].sudo().search([('service_id','=',rec.name)])
                if not existing_job_card:
                    job_card = self.env['job.card'].sudo().create({
                        'service_id':rec.id,
                        'partner_id':rec.partner_id.id,
                        'vehical_id':rec.vehical_id.id,
                        'workshop_id':rec.workshop_id.id,
                        'machanics_id':rec.workshop_id.Workshop_manager_id.id,
                        'make_id' : rec.vehical_id.model_id.brand_id.id,
                        'vehical_model_id':rec.vehical_id.model_id.id,
                        'year' : rec.vehical_id.model_id.model_year,
                        'license_plate' : rec.vehical_id.license_plate,
                        'color' : rec.vehical_id.color,
                        'odometer' : rec.vehical_id.odometer,
                        'package_id':rec.package_id.id,
                        'service_category_id':rec.package_id.service_category_id.id,
                        'service_checklist_id':rec.package_id.service_category_id.checklist_id.id,
                        })
                    job_card._onchange_package_id()
                    job_card._onchange_service_checklist_id()


    def action_request_cancel(self):
        for rec in self:
            rec.status = 'cancelled'

