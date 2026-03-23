from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BeautyMasterSchedule(models.Model):
    _name = 'beauty.master.schedule'
    _description = 'Master Working Schedule'
    _order = 'day_of_week, hour_from'

    master_id = fields.Many2one(
        'res.partner', 
        string="Master", 
        domain="[('is_master', '=', True)]", 
        required=True, 
        ondelete='cascade'
    )
    day_of_week = fields.Selection([
        ('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'),
        ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')
    ], string="Day of Week", required=True)
    
    hour_from = fields.Float(string="Work From", required=True)
    hour_to = fields.Float(string="Work To", required=True)

    @api.constrains('hour_from', 'hour_to')
    def _check_hours(self):
        for rec in self:
            if rec.hour_from >= rec.hour_to:
                raise ValidationError("Start hour must be earlier than end hour!")