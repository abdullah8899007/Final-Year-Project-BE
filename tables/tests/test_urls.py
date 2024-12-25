from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from custom_user.models import User
from tables.models import Table, Reservation
from datetime import datetime, timedelta
import json
from django.core.files import File

class AuthenticatedAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class TableAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.table1 = Table.objects.create(table_number=1,seating_size=4,status="Available")
        self.table2 = Table.objects.create(table_number=2,seating_size=4,status="Available")
        self.url = reverse('tables:tables-list')

    def test_get_tables(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)
    
    def test_create_table(self):
        data = {"table_number":3,"seating_size":8,"status":"Available"}
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Table.objects.filter(seating_size=8).exists())
        self.assertEqual(len(response.json()), 3)
    
    def test_retrieve_table(self):
        url = reverse('tables:tables-detail', args=[self.table1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['table_number'], 1)

    def test_update_table(self):
        url = reverse('tables:tables-detail', args=[self.table1.id])
        data = {'table_number': 5}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Table.objects.get(id=self.table1.id).table_number, 5)

    def test_delete_table(self):
        url = reverse('tables:tables-detail', args=[self.table1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Table.objects.count(), 1)

class ReservationAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.table1 = Table.objects.create(table_number=1,seating_size=4,status="Available")
        self.table2 = Table.objects.create(table_number=2,seating_size=4,status="Available")
        self.table3 = Table.objects.create(table_number=3,seating_size=4,status="Available")
        self.reservation1 = Reservation.objects.create(user='Faaiz', table=self.table1, booking_time="2024-03-03", status="Confirmed")
        self.reservation2 = Reservation.objects.create(user='Ali', table=self.table2, booking_time="2024-03-03", status="Confirmed")
        self.url = reverse('tables:reservations-list')

    def test_get_reservation(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)
    
    def test_create_reservation(self):
        data = {"user":'Faaiz Ali Tariq', "table_id":3, "booking_time":"2024-04-04T12:00:00", "status":"Confirmed"}
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Reservation.objects.filter(user="Faaiz Ali Tariq").exists())
        self.assertEqual(len(response.json()), 3)
    
    def test_retrieve_reservation(self):
        url = reverse('tables:reservations-detail', args=[self.reservation1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['user'], "Faaiz")

    def test_update_reservation(self):
        url = reverse('tables:reservations-detail', args=[self.reservation1.id])
        data = {'user': "FaaizAli"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.get(id=self.reservation1.id).user, "FaaizAli")

    def test_delete_reservation(self):
        url = reverse('tables:reservations-detail', args=[self.reservation1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 1)
