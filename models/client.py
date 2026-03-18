from dateutil.relativedelta import relativedelta
from odoo import models, fields, api

class BeautySalonClient(models.Model):
    _name = 'beauty.salon.client'
    _description = 'Beauty Salon Client'
    _inherit = ['image.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Full Name', required=True, tracking=True, translate=True)
    phone = fields.Char(string='Phone Number', tracking=True)
    email = fields.Char(string='Email')
    
    appointment_ids = fields.One2many(
        comodel_name='beauty.salon.appointment',
        inverse_name='client_id',
        string='Appointments History'
    )
    
    last_visit_date = fields.Datetime(
        string='Last Visit', 
        compute='_compute_last_visit_date', 
        store=True
    )

    @api.depends('appointment_ids.datetime_start', 'appointment_ids.state')
    def _compute_last_visit_date(self):
        """Automatically calculates the date of the last 'done' appointment."""
        for client in self:
            done_appointments = client.appointment_ids.filtered(lambda a: a.state == 'done')
            if done_appointments:
                sorted_appointments = done_appointments.sorted(key=lambda a: a.datetime_start, reverse=True)
                client.last_visit_date = sorted_appointments[0].datetime_start
            else:
                client.last_visit_date = False

    @api.model
    def _cron_send_reminders(self):
        """
        Scheduled action method.
        Finds clients who haven't visited in 30 days and creates a To-Do activity.
        """
        # Calculate the date 30 days ago
        thirty_days_ago = fields.Datetime.now() - relativedelta(days=30)
        
        # Find clients whose last visit was BEFORE 30 days ago
        domain = [
            ('last_visit_date', '!=', False),
            ('last_visit_date', '<', thirty_days_ago)
        ]
        clients_to_remind = self.search(domain)
        
        for client in clients_to_remind:
            # Check if we already created a reminder to avoid spamming the admin
            existing_activity = self.env['mail.activity'].search([
                ('res_model', '=', self._name),
                ('res_id', '=', client.id),
                ('summary', '=', 'Reminder: Call Client')
            ])
            
            if not existing_activity:
                # Create a new To-Do activity
                client.activity_schedule(
                    activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
                    summary='Reminder: Call Client',
                    note=f'The client {client.name} has not visited for over 30 days. Please call them at {client.phone or "no phone number"} to offer a new service.',
                    user_id=self.env.user.id
                )