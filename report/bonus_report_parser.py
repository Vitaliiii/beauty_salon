from odoo import models, api

class MasterBonusReportParser(models.AbstractModel):
    # The name MUST be 'report.' + module_name + '.' + template_id
    _name = 'report.beauty_salon.report_master_bonus_template'
    _description = 'Master Bonus Report Parser'

    @api.model
    def _get_report_values(self, docids, data=None):
        form = data.get('form_data')
        start_date = form.get('start_date')
        end_date = form.get('end_date')
        master_id = form.get('master_id')

        # Build the search domain for appointments
        domain = [
            ('state', '=', 'done'),
            ('datetime_start', '>=', start_date),
            ('datetime_start', '<=', end_date),
        ]
        if master_id:
            # master_id from read() returns a tuple (id, 'Name')
            domain.append(('master_id', '=', master_id[0]))

        appointments = self.env['beauty.appointment'].search(domain)

        # Group data by master for the template
        masters_data = {}
        for app in appointments:
            m = app.master_id
            if m not in masters_data:
                masters_data[m] = {
                    'total_revenue': 0.0, 
                    'total_bonus': 0.0, 
                    'appointments': []
                }
            masters_data[m]['total_revenue'] += app.total_amount
            masters_data[m]['total_bonus'] += app.master_bonus
            masters_data[m]['appointments'].append(app)

        return {
            'doc_ids': docids,
            'doc_model': 'beauty.bonus.report.wizard',
            'start_date': start_date,
            'end_date': end_date,
            'masters_data': masters_data,
        }