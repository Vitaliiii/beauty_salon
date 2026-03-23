from odoo import models, fields, api

class BonusReportWizard(models.TransientModel):
    _name = 'beauty.bonus.report.wizard'
    _description = 'Wizard for Master Bonus Report'

    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    end_date = fields.Date(string="End Date", required=True, default=fields.Date.context_today)
    master_id = fields.Many2one(
        'res.partner', 
        string="Master", 
        domain="[('is_master', '=', True)]",
        help="Leave empty to generate a report for all masters."
    )

    def action_print_report(self):
        # Gather data from the wizard form to pass to the report
        data = {
            'form_data': self.read()[0],
        }
        # Call the report action defined in XML
        return self.env.ref('beauty_salon.action_report_master_bonus').report_action(self, data=data)