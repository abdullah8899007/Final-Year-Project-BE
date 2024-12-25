from rest_framework.test import APITestCase
from rest_framework import status
from .models import MainBalance,PaymentHistory
from .serializers import MainBalanceSerializer,PaymentHistorySerializer
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase


class MainBalanceViewsetTestCase(APITestCase):
    def setUp(self):
        self.main_balance = MainBalance.objects.create(total_price=600)

    def test_main_balance_list(self):
        response = self.client.get('/main-balances/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = MainBalanceSerializer(instance=self.main_balance)
        self.assertEqual(response.data, serializer.data)
        
        


class PaymentHistoryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payment_history_data = {
            'customer_name': 'Abdullah Khan',
            'data_issued': '2024-02-15T08:00:00Z',
            'payment_type': 'CASH',
            'payment_status': 'PAID'
        }
        self.payment_history = PaymentHistory.objects.create(**self.payment_history_data)
        self.url = reverse('paymenthistory-list')

    def test_payment_history_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = PaymentHistorySerializer(instance=self.payment_history)
        self.assertEqual(response.data[0], serializer.data)

    def test_payment_history_create(self):
        payment_history_data = {
            'customer_name': 'Ali Abdullah',
            'data_issued': '2024-02-16T08:00:00Z',
            'payment_type': 'Card',
            'payment_status': 'PENDING'
        }
        response = self.client.post(self.url, payment_history_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(PaymentHistory.objects.filter(customer_name='Ali Abdullah').exists())

