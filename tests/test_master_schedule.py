from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMasterSchedule(TransactionCase):

    def test_invalid_hours(self):
        """Тест: Система не повинна дозволити Start > End"""
        master = self.env['res.partner'].create({'name': 'Test', 'beauty_role': 'master'})
        
        with self.assertRaises(ValidationError):
            self.env['beauty.master.schedule'].create({
                'master_id': master.id,
                'day_of_week': '1',
                'hour_from': 18.0,
                'hour_to': 9.0  # Помилка: кінець раніше початку
            })