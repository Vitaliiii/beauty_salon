from odoo import models, fields, api

class BeautyReview(models.Model):
    _name = 'beauty.review'
    _description = 'Client Review'
    _order = 'create_date desc'

    appointment_id = fields.Many2one(
        'beauty.appointment', 
        string="Appointment", 
        required=True, 
        domain="[('state', '=', 'done')]"
    )
    client_id = fields.Many2one(related='appointment_id.client_id', store=True, readonly=True)
    master_id = fields.Many2one(related='appointment_id.master_id', store=True, readonly=True)
    
    rating = fields.Selection([
        ('1', 'Terrible'), ('2', 'Poor'), ('3', 'Fair'), ('4', 'Good'), ('5', 'Excellent')
    ], string="Rating", required=True, default='5')
    
    comment = fields.Text(string="Comment")