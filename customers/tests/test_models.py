from django.test import TestCase
from customers.models import CustomersModel

class CustomersModelTestCase(TestCase):
    def setUp(self):
        CustomersModel.objects.create(
            name="John Doe",
            phone="1234567890",
            email="john@example.com",
            address="123 Main St"
        )

    def test_customer_creation(self):
        customer = CustomersModel.objects.get(name="John Doe")
        self.assertEqual(customer.phone, "1234567890")
        self.assertEqual(customer.email, "john@example.com")
        self.assertEqual(customer.address, "123 Main St")


       