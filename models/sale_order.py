from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"

    job_card_id = fields.Many2one(
        'job.card',
        string='Job Card'
    )
    vehicle_id = fields.Many2one(
        comodel_name = "vehicle.detail",
        string = "Vehicle",
        required = True,
    )
    is_package_so = fields.Boolean(
        string ="Package Create"
    )


    @api.onchange('is_package_so')
    def _onchange_is_package_so(self):

        if self.is_package_so:
            self.order_line = [(5,0,0)]



    def action_confirm(self):
        res = super().action_confirm()

        for rec in self:
            for line in rec.order_line:

                product = line.product_template_id

                if product.is_service_package and rec.is_package_so == True:
                    start_date = fields.Date.today()
                    expiry_date = start_date + relativedelta(
                        months=product.duration
                    )

                    self.env['service.package.history'].sudo().create({
                        'partner_id': rec.partner_id.id,
                        'sale_order_id': rec.id,
                        'vehicle_id': rec.vehicle_id.id,
                        'package_id': product.id,
                        'start_date': start_date,
                        'expired_date': expiry_date,
                        'state': 'draft',
                    })

        return res