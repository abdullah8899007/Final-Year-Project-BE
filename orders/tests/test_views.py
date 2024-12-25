from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from orders.models import Orders, Invoice
from orders.serializers import OrdersSerializer, InvoiceSerializer
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from customers.models import CustomersModel


class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


class UpdateOrderViewSetTestCase(AuthenticatedAPITestCase):

    def test_retrieve_order(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        order = Orders.objects.create(
            customer_id=customer.pk,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType="Dinner",
            total=100
        )
        response = self.client.get(reverse('orders:orders-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_order(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        order = Orders.objects.create(
            customer=customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType="Dinner",
            total=100
        )
        updated_data = {
            'customer': customer.pk,
            'status': 'Ready'
        }
        response = self.client.put(reverse('orders:orders-detail', args=[order.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_order(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        order = Orders.objects.create(
            customer_id=customer.pk,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType="Lunch",
            total=100
        )
        response = self.client.delete(reverse('orders:orders-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_order_with_required_fields(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        data = {
            'customerId': customer.pk,
            'items': {"item1": 1},
            'orderType': 'Dinner',
            'total': 100
        }
        response = self.client.post(reverse('orders:orders-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_with_all_fields(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        data = {
            'customerId': customer.pk,
            'items': {"item1": 1},
            'deals': {"deal1": 2},
            'status': 'Enqueue',
            'orderType': 'Dinner',
            'total': 100
        }
        response = self.client.post(reverse('orders:orders-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class InvoiceViewSetTestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.create_order_url = reverse('orders:orders-list')
        self.create_invoice_url = reverse('orders:invoices-list')


    def test_retrieve_invoice(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        order = Orders.objects.create(
            customer=customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType="Dinner",
            total=100
        )
        invoice = Invoice.objects.create(order=order)
        response = self.client.get(reverse('orders:invoices-detail', args=[invoice.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_order_success(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        data = {
            'customerId': customer.pk,
            'items': {"item1": 1},  
            'deals': {"deal1": 2}, 
            'status': 'Enqueue',
            'orderType': 'Dinner',
            'total': 100
        }
        response = self.client.post(self.create_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_order_missing_fields(self):
        data = {
            'items': {"item1": 1},
            'deals': {"deal1": 2},
            'status': 'Enqueue',
            'orderType': 'Dinner',
            'total': 100
        }
        response = self.client.post(self.create_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_invoice_invalid_order(self):
        data = {
            'order': 9999,
            'issued_at': '2024-02-15T12:00:00Z'
        }
        response = self.client.post(self.create_invoice_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)