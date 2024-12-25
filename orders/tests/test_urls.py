from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from customers.models import CustomersModel
from orders.models import Orders, Invoice
from orders.serializers import OrdersSerializer, InvoiceSerializer
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Orders, Invoice
from orders.serializers import OrdersSerializer, InvoiceSerializer
from django.urls import reverse as django_reverse




class AuthenticatedAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


class TestOrderEndpoints(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        self.create_order_url = django_reverse('orders:orders-list')
        self.create_invoice_url = django_reverse('orders:invoices-list')

    def test_order_list_url(self):
        url = reverse('orders:orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_orders(self):
        order = Orders.objects.create(
            customer=self.customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType ="Dinner",
            total =100
        )
        url = reverse('orders:orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 1)

    def test_list_invoices(self):
        order = Orders.objects.create(
            customer=self.customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType ="Dinner",
            total =100
        )
        invoice = Invoice.objects.create(order=order)
        url = reverse('orders:invoices-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["data"]), 1)


    def test_invalid_order_detail_url(self):
        order_id = 9999 
        url = reverse('orders:orders-detail', kwargs={'pk': order_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_invalid_invoice_detail_url(self):
        invoice_id = 9999  
        url = reverse('orders:invoices-detail', kwargs={'pk': invoice_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)







