# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestBeautyAppointment(TransactionCase):

    def setUp(self):
        """Set up initial data for the tests"""
        super(TestBeautyAppointment, self).setUp()
        
        # Create a test service: 1 hour duration, 1000 UAH price
        self.service = self.env['beauty.salon.service'].create({
            'name': 'Test Haircut',
            'price': 1000.0,
            'duration': 1.0
        })
        
        # Create a test master with a 10% bonus percentage
        self.master = self.env['beauty.salon.master'].create({
            'name': 'Test Master',
            'bonus_percentage': 10.0
        })
        
        # Create a test client
        self.client = self.env['beauty.salon.client'].create({
            'name': 'Test Client'
        })

    def test_01_calculation_logic(self):
        """Test automatic calculation of end time, total amount, and master bonus"""
        start_time = datetime(2026, 5, 20, 10, 0, 0)
        
        # Create an appointment with the predefined service
        appointment = self.env['beauty.salon.appointment'].create({
            'client_id': self.client.id,
            'master_id': self.master.id,
            'service_ids': [(4, self.service.id)],
            'datetime_start': start_time,
        })

        # Verify end time calculation: 10:00 + 1.0 hour = 11:00
        expected_end = start_time + timedelta(hours=1.0)
        self.assertEqual(appointment.datetime_end, expected_end, 
                         "Error: End time calculation is incorrect!")

        # Verify total amount: should be 1000.0 UAH
        self.assertEqual(appointment.total_amount, 1000.0, 
                         "Error: Total amount calculation is incorrect!")

        # Verify master bonus: 10% of 1000.0 = 100.0 UAH
        self.assertEqual(appointment.master_bonus, 100.0, 
                         "Error: Master bonus calculation is incorrect!")

    def test_02_overlapping_appointment(self):
        """Test the prevention of overlapping appointments for the same master (Constraints)"""
        start_time = datetime(2026, 5, 20, 14, 0, 0)
        
        # Create the first appointment at 14:00 (ends at 15:00)
        self.env['beauty.salon.appointment'].create({
            'client_id': self.client.id,
            'master_id': self.master.id,
            'service_ids': [(4, self.service.id)],
            'datetime_start': start_time,
        })

        # Attempt to create a second appointment at 14:30 for the same master
        # The system must raise a ValidationError due to time overlap
        with self.assertRaises(ValidationError, 
                               msg="Error: The system should have blocked overlapping appointments!"):
            self.env['beauty.salon.appointment'].create({
                'client_id': self.client.id,
                'master_id': self.master.id,
                'service_ids': [(4, self.service.id)],
                'datetime_start': start_time + timedelta(minutes=30),
            })