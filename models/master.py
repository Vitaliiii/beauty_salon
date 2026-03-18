from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BeautySalonMaster(models.Model):
    _name = 'beauty.salon.master'
    _description = 'Beauty Salon Master'
    _inherit = ['image.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Full Name', required=True, tracking=True, translate=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    
    user_id = fields.Many2one('res.users', string='System User')
    
    bonus_percentage = fields.Float(
        string='Bonus Percentage (%)', 
        required=True, 
        default=30.0,
        tracking=True
    )
    
    specialty_ids = fields.Many2many(
        comodel_name='beauty.salon.service',
        string='Specialties (Services)'
    )

    active = fields.Boolean(string='Active', default=True)

    @api.constrains('bonus_percentage')
    def _check_bonus_percentage(self):
        """Перевірка, щоб відсоток бонусу був від 0 до 100"""
        for rec in self:
            if rec.bonus_percentage < 0 or rec.bonus_percentage > 100:
                raise ValidationError(_("Bonus percentage must be between 0 and 100!"))