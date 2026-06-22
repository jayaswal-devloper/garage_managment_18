from odoo import api, fields, models

class VehicalDiagnosis(models.Model):
    _name = "vehicle.diagnosis"
    _inherit = ['mail.thread']
    _description = "Vehicle Inspection and Diagnosis"
    _rec_name = 'job_card_id'

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
    state = fields.Selection(
        [('new','New'),('confirmed','Confirmed')],
        default='new'
    )
    job_card_service_charge_line_ids = fields.One2many(
        comodel_name = 'job.card.service.charge.line',
        inverse_name = 'diagnosis_id'  
    )
    job_card_vehicle_part_ids = fields.One2many(
        comodel_name = 'job.card.vehicle.spare.parts',
        inverse_name = 'diagnosis_id' 
    )
    purchase_order_count = fields.Integer(
        compute="_compute_order_counts"
    )

    sale_order_count = fields.Integer(
        compute="_compute_order_counts"
    )
    

    @api.depends()
    def _compute_order_counts(self):
        PurchaseOrder = self.env['purchase.order']
        SaleOrder = self.env['sale.order']

        for rec in self:
            rec.purchase_order_count = PurchaseOrder.search_count([
                ('job_card_id', '=', rec.job_card_id.id)
            ])

            rec.sale_order_count = SaleOrder.search_count([
                ('job_card_id', '=', rec.job_card_id.id)
            ])


    def create_purchase_rfq(self):

        order_lines = []

        vendor = False

        for line in self.job_card_vehicle_part_ids:

            seller = line.product_id.seller_ids[:1]

            if seller:
                vendor = seller.partner_id

            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.quantity,
                'price_unit': line.unit_price,
                'product_uom': line.uom_id.id,
                'date_planned': fields.Datetime.now(),
                'name': line.product_id.display_name,
            }))

        purchase = self.env['purchase.order'].create({
            'partner_id': self.job_card_id.partner_id.id,
            'job_card_id':self.job_card_id.id,
            'order_line': order_lines,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'res_id': purchase.id,
            'view_mode': 'form',
            'target': 'current',
        }


    def create_sale_order(self):

        order_lines = []

        for line in self.job_card_service_charge_line_ids:
            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'price_unit': line.unit_price,
            }))

        for line in self.job_card_vehicle_part_ids:
            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'price_unit': line.unit_price,
            }))

        sale_order = self.env['sale.order'].create({
            'partner_id': self.job_card_id.partner_id.id,
            'job_card_id':self.job_card_id.id,
            'order_line': order_lines,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }


    def confirm_diagnosis(self):
        for rec in self:
            rec.state = 'confirmed'
            rec.job_card_id.state = 'in_progress'

            



    def action_view_purchase_orders(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Orders',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('job_card_id', '=', self.job_card_id.id)],
            'context': {
                'default_job_card_id': self.job_card_id.id,
            }
        }

    def action_view_sale_orders(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('job_card_id', '=', self.job_card_id.id)],
            'context': {
                'default_job_card_id': self.job_card_id.id,
            }
        }