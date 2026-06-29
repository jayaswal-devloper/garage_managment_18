from odoo import api, fields, models
from odoo.exceptions import ValidationError

class JobCard(models.Model):
    _name = 'job.card'
    _description = 'Every request are confirm then create a job card'
    _inherit = ['mail.thread']
    

    name = fields.Char(
        string="Job Number",
        default="New",
        readonly=True,
        copy=False
    )
    service_id = fields.Many2one(
        comodel_name="service.request",
        string="Service Request",
        readonly=True,
        copy=False
    )
    partner_id = fields.Many2one(
        comodel_name = "res.partner",
        string = "Customer",
        readonly=True,
        copy=False
    )
    vehical_id = fields.Many2one(
        comodel_name = "vehicle.detail",
        string="Vehicle",
        readonly=True,
        copy=False
    )
    workshop_id = fields.Many2one(
        comodel_name = "vehical.workshop",
        string="Workshop",
        readonly=True,
        copy=False
    )
    machanics_id = fields.Many2one(
        comodel_name="hr.employee",
        string = "Assigned Mechanic",
        readonly=True,
    )
    description = fields.Text(
        string = "Description"
    )
    package_id = fields.Many2one(
        comodel_name = "service.packages",
        string = "Service Package",
        readonly = True,
        copy=False
    )
    make_id = fields.Many2one(
        comodel_name = "garage.vehicle.make",
        string = "Make",
        readonly=True,
        copy=False
    )
    vehical_model_id = fields.Many2one(
        comodel_name = "garage.vehicle.model",
        string="Vehicle Model",
        readonly=True,
        copy=False
    )
    year = fields.Char(
        string = "Year",
        readonly=True,
        copy=False
    )       
    license_plate = fields.Char(
        string="License Plate",
        readonly=True,
        copy=False
    )
    color = fields.Char(
        string="Color",
        readonly=True,
        copy=False
    )
    odometer = fields.Float(
        string="Odometer",
        readonly=True,
        copy=False
    )
    service_type_ids = fields.Many2many(
        comodel_name="service.type",
        string = "Service Type"
    )
    service_category_id = fields.Many2one(
        comodel_name = "service.category",
        string="Service Category"
    )
    vehical_repaird = fields.Boolean(
        string="Vehicle Repaired"
    )
    state = fields.Selection(
        [('received','Received'),('in_progress','In Progress'),('done','Done')],
        default='received'
    )
    service_checklist_id = fields.Many2one(
        comodel_name = "service.checklist",
        string = "Checklist Template "
    )
    job_card_checklist_line_ids = fields.One2many(
        comodel_name = "job.card.checklist.line",
        inverse_name = "job_card_id"
    )
    job_card_service_charge_line_ids = fields.One2many(
        comodel_name = "job.card.service.charge.line",
        inverse_name = "job_card_id"
    )
    spare_parts_ids = fields.One2many(
        comodel_name = "job.card.vehicle.spare.parts",
        inverse_name = "job_card_id"
    )
    job_timesheet_ids = fields.One2many(
        comodel_name = "job.card.timesheet.line",
        inverse_name = "job_card_id"
    )
    
    checklist_percentage = fields.Float(
        string="Checklist %",
        compute="_compute_checklist_percentage",
        store=True
    )
    checklist_done_cont = fields.Integer(
        compute="_compute_job_card_checklist_line_count"
    )
    diagnosis_cont = fields.Integer(
        compute="_compute_vehical_diagnosis_count"
    )
    work_order_cont = fields.Integer(
        compute="_compute_work_order_count"
    )
    job_image_ids = fields.One2many(
        comodel_name = "job.card.image",
        inverse_name = "job_card_id"
    )

    customer_rating = fields.Selection([
        ('0','0 star'),
        ('1','1 star'),
        ('2','2 star'),
        ('3','3 star'),
        ('4','4 star'),
        ('5','5 star'),],
        string = "Customer Rating",
        default = "0"
    )
    customer_description = fields.Text(
        string = "Review" 
    )

    @api.onchange('service_category_id')
    def _onchange_service_category_id(self):
        if self.service_category_id:
            self.service_checklist_id = self.service_category_id.checklist_id.id
        else:
            self.service_checklist_id = ""

    @api.onchange('service_checklist_id')
    def _onchange_service_checklist_id(self):
        self.job_card_checklist_line_ids = [(5,0,0)]

        if self.service_checklist_id:
            lines = []

            for item in self.service_checklist_id.checklist_itme_ids:
                lines.append((0,0,{
                    'name':item.name,
                    'sequence':item.sequence,
                    'description':item.description,
                    'required':item.required,
                    }))
            self.job_card_checklist_line_ids = lines


    @api.onchange('package_id')
    def _onchange_package_id(self):
        self.job_card_service_charge_line_ids = [(5,0,0)]

        if self.package_id:
            lines = []

            for item in self.package_id.service_package_line_ids:
                lines.append((0,0,{
                    'product_id':item.product_id.id,
                    'uom_id':item.uom_id.id,
                    'unit_price':item.list_price
                    }))
            self.job_card_service_charge_line_ids = lines



    @api.depends('job_card_checklist_line_ids.done')
    def _compute_checklist_percentage(self):
        for rec in self:
            total = len(rec.job_card_checklist_line_ids)
            if total:
                completed = len(
                    rec.job_card_checklist_line_ids.filtered(lambda l: l.done)
                )
                rec.checklist_percentage = (completed / total) * 100
            else:
                rec.checklist_percentage = 0.0

                
    @api.model
    def create(self,vals_list):
        if vals_list.get('name','New') == 'New':
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'garage.job.card'
                )
            return super().create(vals_list)


    def _compute_job_card_checklist_line_count(self):
        for rec in self:
            rec.checklist_done_cont = self.env['job.card.checklist.line'].search_count([
                ('job_card_id', '=', rec.id),
                ('done','=',True)
            ])

    def _compute_vehical_diagnosis_count(self):
        for rec in self:
            rec.diagnosis_cont = self.env['vehicle.diagnosis'].search_count([
                    ('job_card_id','=',self.id)
                ])

    def _compute_work_order_count(self):
        for rec in self:
            rec.work_order_cont = self.env['work.orders'].search_count([
                    ('job_card_id','=',self.id),
                ])

    def action_view_job_card_checklist_line(self):
        return{
            'type':'ir.actions.act_window',
            'name': 'Job Cards',
            'res_model': 'job.card.checklist.line',
            'view_mode': 'list,form',
            'domain': [('job_card_id', '=', self.id),
                        ('done','=',True)
                      ],
        }

    def action_view_vehical_diagnosis(self):

        return{
            'type':'ir.actions.act_window',
            'name':'Diagnosis',
            'res_model':'vehicle.diagnosis',
            'view_mode':'list,form',
            'domain':[
                        ('job_card_id','=',self.id)
                     ]
        }

    def action_view_work_orders(self):
        return{
            'type':'ir.actions.act_window',
            'name': 'Work Order',
            'res_model': 'work.orders',
            'view_mode': 'list,form',
            'domain': [
                        ('job_card_id', '=', self.id),
                      ],
        }

    def service_diagnosis(self):
        
        return{
            'type':'ir.actions.act_window',
            'res_model':'diagnosis.wizard',
            'view_mode':'form',
            'target' : 'new',
            'context':{
                'default_job_card_id': self.id,
                'default_machanics_id': self.machanics_id.id,
                'default_job_card_service_charge_line_ids': [
                                (6, 0, self.job_card_service_charge_line_ids.ids)
                    ]
                }
            }



    def create_work_order(self):
        for rec in self:
            if not rec.job_timesheet_ids.ids:
                raise ValidationError("Are you Missing a value in the job timesheet. ")
            if rec.name:
                existing_work_order = self.env['work.orders'].sudo().search([('job_card_id','=',rec.name)])
                if existing_work_order:
                    raise ValidationError("Your work order Report are already created.")
                else:
                    work_order = self.env['work.orders'].sudo().create({
                        'job_card_id':rec.id,
                        'machanics_id':rec.machanics_id.id,
                        })
                    work_order._onchange_job_card_id()

                    

    def job_card_done_button(self):
        for rec in self:
            rec.state = 'done'




    def send_rating_request(self):
        template = self.env.ref('garage_managment.mail_template_send_review_request')

        for rec in self:
            if rec.partner_id and rec.partner_id.email:
                template.send_mail(rec.id, force_send=True)