from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from tables.models import Table, Reservation


class TableModelTestCase(TestCase):
    def test_table_creation(self):
        table1 = Table.objects.create(table_number=1,seating_size=4,status="Available")
        self.assertEqual(table1.table_number, 1)


class ReservationModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(table_number=2,seating_size=4,status="Available")

    def test_reservation_creation(self):
        self.reservation1 = Reservation.objects.create(user='Faaiz', table=self.table, booking_time="2024-03-03", status="Confirmed")
        self.assertEqual(self.reservation1.table, self.table)
