from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import reverse
from customers.views import CustomerViewSet
from customers.models import CustomersModel
from customers.serializers import CustomerSerializer

class CustomerURLsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.customer = CustomersModel.objects.create(
            name="John Doe",
            phone="1234567890",
            email="john@example.com",
            address="123 Main St"
        )
        self.customer_serializer_data = CustomerSerializer(instance=self.customer).data

    def test_customer_list_url(self):
        url = reverse('customer-list')
        request = self.factory.get(url)
        response = CustomerViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_customer_detail_url(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.pk})
        request = self.factory.get(url)
        response = CustomerViewSet.as_view({'get': 'retrieve'})(request, pk=self.customer.pk)
        self.assertEqual(response.status_code, 200)

    def test_customer_create_url(self):
        url = reverse('customer-list')
        request_data = {
            'name': 'Jane Doe',
            'phone': '0987654321',
            'email': 'jane@example.com',
            'address': '456 Elm St'
        }
        request = self.factory.post(url, request_data, format='json')
        response = CustomerViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

    def test_customer_update_url(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.pk})
        request_data = {
            'name': 'John Doe Updated',
            'phone': '9999999999',
            'email': 'john_updated@example.com',
            'address': '789 Oak St'
        }
        request = self.factory.put(url, request_data, format='json')
        response = CustomerViewSet.as_view({'put': 'update'})(request, pk=self.customer.pk)
        self.assertEqual(response.status_code, 200)
        # Verify if the customer data is updated
        updated_customer = CustomersModel.objects.get(pk=self.customer.pk)
        self.assertEqual(updated_customer.name, request_data['name'])

    def test_customer_delete_url(self):
        url = reverse('customer-detail', kwargs={'pk': self.customer.pk})
        request = self.factory.delete(url)
        response = CustomerViewSet.as_view({'delete': 'destroy'})(request, pk=self.customer.pk)
        self.assertEqual(response.status_code, 204)
        # Verify if the customer is deleted
        with self.assertRaises(CustomersModel.DoesNotExist):
            CustomersModel.objects.get(pk=self.customer.pk)
