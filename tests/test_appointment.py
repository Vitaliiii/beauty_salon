from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime

class TestBeautyAppointment(TransactionCase):

    def setUp(self):
        """Підготовка даних для тестів"""
        super(TestBeautyAppointment, self).setUp()
        
        # Створюємо послугу
        self.service = self.env['beauty.service'].create({
            'name': 'Test Haircut',
            'price': 1000.0,
            'duration': 1.0
        })
        
        # Створюємо майстра з бонусом 20%
        self.master = self.env['res.partner'].create({
            'name': 'Master Test',
            'beauty_role': 'master',
            'bonus_percentage': 20.0
        })
        
        # Створюємо клієнта
        self.client = self.env['res.partner'].create({
            'name': 'Client Test',
            'beauty_role': 'client'
        })

        # Додаємо графік: Понеділок (0), 09:00 - 18:00
        self.env['beauty.master.schedule'].create({
            'master_id': self.master.id,
            'day_of_week': '0',
            'hour_from': 9.0,
            'hour_to': 18.0
        })

    def test_01_calculation_logic(self):
        """Тест: Чи правильно рахується сума та бонус"""
        # 2026-03-02 — це понеділок
        appointment = self.env['beauty.appointment'].create({
            'client_id': self.client.id,
            'master_id': self.master.id,
            'service_ids': [(4, self.service.id)],
            'datetime_start': datetime(2026, 3, 2, 10, 0, 0)
        })
        
        self.assertEqual(appointment.total_amount, 1000.0, "Ціна має бути 1000")
        self.assertEqual(appointment.master_bonus, 200.0, "Бонус має бути 20% від 1000 = 200")

    def test_02_schedule_constraint(self):
        """Тест: Чи викидає помилку запис на 22:00 (поза графіком)"""
        with self.assertRaises(ValidationError):
            self.env['beauty.appointment'].create({
                'client_id': self.client.id,
                'master_id': self.master.id,
                'service_ids': [(4, self.service.id)],
                'datetime_start': datetime(2026, 3, 2, 22, 0, 0) # Поза графіком
            })