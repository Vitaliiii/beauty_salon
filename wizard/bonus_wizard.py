from odoo import models, fields, api

class BeautySalonBonusWizard(models.TransientModel):
    _name = 'beauty.salon.bonus.wizard'
    _description = 'Master Bonus Calculation Wizard'

    master_id = fields.Many2one('beauty.salon.master', string='Master', required=True)
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)

    def action_print_report(self):
        """Generates the PDF report"""
        return self.env.ref('beauty_salon.action_report_master_bonus').report_action(self)