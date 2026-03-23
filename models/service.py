from odoo import models, fields

class BeautyService(models.Model):
    _name = 'beauty.service'
    _description = 'Beauty Salon Service'

    name = fields.Char(string="Service Name", required=True, translate=True)
    description = fields.Text(string="Description", translate=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    price = fields.Monetary(string="Price", required=True, default=0.0)
    
    duration = fields.Float(
        string="Duration (hours)", 
        required=True, 
        default=1.0,
        help="Specify duration in hours (e.g., 1.5 for an hour and a half)."
    )