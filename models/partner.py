from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # --- Roles Logic ---
    beauty_role = fields.Selection([
        ('client', 'Client'),
        ('master', 'Master'),
        ('both', 'Master & Client')
    ], string="Salon Role", default='client')

    is_client = fields.Boolean(
        string="Is Client", 
        compute="_compute_beauty_roles", 
        store=True
    )
    is_master = fields.Boolean(
        string="Is Master", 
        compute="_compute_beauty_roles", 
        store=True
    )

    @api.depends('beauty_role')
    def _compute_beauty_roles(self):
        for rec in self:
            rec.is_client = rec.beauty_role in ['client', 'both']
            rec.is_master = rec.beauty_role in ['master', 'both']

    # --- Master Specific Fields ---
    master_user_id = fields.Many2one(
        'res.users', 
        string="System User (Master)", 
        help="Linked user account for system access."
    )
    bonus_percentage = fields.Float(
        string="Bonus Percentage (%)", 
        default=30.0,
        help="Percentage the master receives from the service price."
    )
    specialty_ids = fields.Many2many(
        'beauty.service', 
        string="Specialties (Services)",
        help="Services this master can provide."
    )
    
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', 
        default=lambda self: self.env.company.currency_id
    )
    
    earned_bonus = fields.Monetary(
        string="Total Earned Bonus", 
        compute="_compute_earned_bonus", 
        store=True
    )
    
    # --- Master Relations (History, Schedule, Reviews) ---
    master_appointment_ids = fields.One2many(
        'beauty.appointment', 
        'master_id', 
        string="Master Appointments"
    )

    master_schedule_ids = fields.One2many(
        'beauty.master.schedule', 
        'master_id', 
        string="Working Hours"
    )

    review_ids = fields.One2many(
        'beauty.review', 
        'master_id', 
        string="Reviews"
    )

    @api.depends('master_appointment_ids.master_bonus', 'master_appointment_ids.state')
    def _compute_earned_bonus(self):
        for partner in self:
            # Нараховуємо бонуси лише за виконані візити
            done_appointments = partner.master_appointment_ids.filtered(lambda a: a.state == 'done')
            partner.earned_bonus = sum(done_appointments.mapped('master_bonus'))

    # --- Client Specific Fields ---
    client_appointment_ids = fields.One2many(
        'beauty.appointment', 
        'client_id', 
        string="Appointment History"
    )
    last_visit_date = fields.Date(
        string="Last Visit Date", 
        compute="_compute_last_visit_date", 
        store=True
    )

    @api.depends('client_appointment_ids.datetime_start', 'client_appointment_ids.state')
    def _compute_last_visit_date(self):
        for partner in self:
            done_appointments = partner.client_appointment_ids.filtered(
                lambda a: a.state == 'done' and a.datetime_start
            )
            if done_appointments:
                # Знаходимо найпізнішу дату серед виконаних візитів
                latest_appointment = max(done_appointments, key=lambda a: a.datetime_start)
                partner.last_visit_date = latest_appointment.datetime_start.date()
            else:
                partner.last_visit_date = False