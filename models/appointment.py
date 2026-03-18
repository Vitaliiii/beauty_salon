# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BeautySalonAppointment(models.Model):
    _name = 'beauty.salon.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Beauty Salon Appointment'
    _order = 'datetime_start desc'

    name = fields.Char(string='Reference', readonly=True, copy=False, default=lambda self: _('New'))
    
    client_id = fields.Many2one('beauty.salon.client', string='Client', required=True, tracking=True)
    master_id = fields.Many2one('beauty.salon.master', string='Master', required=True, tracking=True)
    service_ids = fields.Many2many('beauty.salon.service', string='Services', required=True)
    
    datetime_start = fields.Datetime(string='Start Time', required=True, tracking=True)
    
    # Currency context (needed for monetary fields)
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                  default=lambda self: self.env.company.currency_id)
    
    # Fields that use the compute method
    datetime_end = fields.Datetime(string='End Time', compute='_compute_total_amount', store=True)
    
    total_amount = fields.Monetary(string='Total Amount', currency_field='currency_id', 
                                   compute='_compute_total_amount', store=True, tracking=True)
    
    master_bonus = fields.Monetary(string='Master Bonus', currency_field='currency_id', 
                                   compute='_compute_total_amount', store=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    @api.depends('service_ids', 'datetime_start', 'master_id.bonus_percentage')
    def _compute_total_amount(self):
        """Calculates end time, total amount, and master's bonus in one go."""
        for rec in self:
            # 1. Calculation of Finances
            total = sum(rec.service_ids.mapped('price'))
            rec.total_amount = total
            
            # 2. Calculation of Master Bonus
            bonus_percent = rec.master_id.bonus_percentage or 0.0
            rec.master_bonus = (total * bonus_percent) / 100.0
            
            # 3. Calculation of End Time (sum of all service durations)
            duration = sum(rec.service_ids.mapped('duration'))
            if rec.datetime_start:
                rec.datetime_end = rec.datetime_start + fields.Timedelta(hours=duration)
            else:
                rec.datetime_end = False

    # Constraints for overlapping schedules
    @api.constrains('datetime_start', 'datetime_end', 'master_id')
    def _check_master_availability(self):
        for rec in self:
            if rec.datetime_start and rec.datetime_end:
                overlap = self.search([
                    ('id', '!=', rec.id),
                    ('master_id', '=', rec.master_id.id),
                    ('state', 'not in', ['cancelled']),
                    ('datetime_start', '<', rec.datetime_end),
                    ('datetime_end', '>', rec.datetime_start),
                ])
                if overlap:
                    raise ValidationError(_("This master is already booked for the selected time period!"))

    # State management actions
    def action_confirm(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'confirmed'

    def action_done(self):
        for rec in self:
            if rec.state == 'confirmed':
                rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    # Sequence generation
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('beauty.salon.appointment') or _('New')
        return super().create(vals_list)