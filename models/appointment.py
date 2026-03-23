from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class BeautyAppointment(models.Model):
    _name = 'beauty.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Number", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    client_id = fields.Many2one('res.partner', string="Client", domain="[('is_client', '=', True)]", required=True, tracking=True)
    master_id = fields.Many2one('res.partner', string="Master", domain="[('is_master', '=', True)]", required=True, tracking=True)
    service_ids = fields.Many2many('beauty.service', string="Services", required=True)
    datetime_start = fields.Datetime(string="Start Time", required=True, tracking=True)
    datetime_end = fields.Datetime(string="End Time", compute="_compute_datetime_end", store=True)
    state = fields.Selection([
        ('draft', 'New'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancelled', 'Cancelled')
    ], default='draft', required=True, tracking=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    total_amount = fields.Monetary(string="Total", compute="_compute_totals", store=True)
    master_bonus = fields.Monetary(string="Master Bonus", compute="_compute_totals", store=True)

    # Логіка автоматичного номера (Sequence)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('beauty.appointment') or _('New')
        return super().create(vals_list)

    @api.constrains('datetime_start', 'master_id')
    def _check_master_schedule(self):
        for rec in self:
            if not rec.datetime_start or not rec.master_id:
                continue
            day = str(rec.datetime_start.weekday())
            appt_hour = rec.datetime_start.hour + rec.datetime_start.minute / 60.0
            schedules = self.env['beauty.master.schedule'].search([
                ('master_id', '=', rec.master_id.id),
                ('day_of_week', '=', day)
            ])
            if not schedules:
                raise ValidationError(_("Master %s does not work on this day!") % rec.master_id.name)
            in_hours = any(s.hour_from <= appt_hour <= s.hour_to for s in schedules)
            if not in_hours:
                raise ValidationError(_("The appointment is outside of the master's working hours!"))

    @api.depends('datetime_start', 'service_ids.duration')
    def _compute_datetime_end(self):
        for rec in self:
            if rec.datetime_start and rec.service_ids:
                rec.datetime_end = rec.datetime_start + timedelta(hours=sum(rec.service_ids.mapped('duration')))
            else:
                rec.datetime_end = rec.datetime_start

    @api.depends('service_ids.price', 'master_id.bonus_percentage', 'state')
    def _compute_totals(self):
        for rec in self:
            rec.total_amount = sum(rec.service_ids.mapped('price'))
            rec.master_bonus = rec.total_amount * (rec.master_id.bonus_percentage / 100.0) if rec.master_id else 0.0