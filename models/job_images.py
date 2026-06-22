from odoo import api, fields, models

class JobCardImage(models.Model):
    _name = "job.card.image"
    _description = "Image of the cars"


    name = fields.Char(
        string = "file Name"
    )
    image_1920 = fields.Image(
        max_width=200,
        max_height=200,
        string="Job Image"
    )
    job_card_id = fields.Many2one(
        comodel_name = "job.card",
        string = "Job Card"
    )