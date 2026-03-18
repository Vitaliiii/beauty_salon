from odoo import models, fields

class BeautySalonService(models.Model):
    _name = 'beauty.salon.service'
    _description = 'Beauty Salon Service'

    name = fields.Char(string='Service Name', required=True, translate=True)
    description = fields.Text(string='Description', translate=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    price = fields.Monetary(string='Price', currency_field='currency_id')
    
    duration = fields.Float(
        string='Duration (Hours)', 
        required=True, 
        default=1.0,
        help="Expected duration of the service in hours."
    )
    
    active = fields.Boolean(string='Active', default=True)