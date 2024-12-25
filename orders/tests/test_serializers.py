from django.test import TestCase
from orders.serializers import OrdersSerializer, InvoiceSerializer
import json 
from orders.models import Orders, Invoice
from customers.models import CustomersModel



class OrdersSerializerTestCase(TestCase):
    def setUp(self):
        self.customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        self.order = Orders.objects.create(
            customer=self.customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType ="Online",
            total =100
        )

    def test_orders_serializer_customer_id(self):
        serializer = OrdersSerializer(instance=self.order)
        self.assertEqual(serializer.data['customerId'], self.customer.id)

    def test_orders_serializer_customer_name(self):
        serializer = OrdersSerializer(instance=self.order)
        self.assertEqual(serializer.data['name'], self.customer.name)


    def test_orders_serializer_fields(self):
        expected_fields = ['id', 'customerId', 'name', 'items', 'deals', 'status', 'orderType', 'total', 'created_at']  # Remove trailing spaces
        serializer = OrdersSerializer(instance=self.order)
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))


class InvoiceSerializerTestCase(TestCase):
    def setUp(self):
        self.customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="Test Address")
        self.order = Orders.objects.create(
            customer=self.customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType ="Online",
            total =100
        )
        self.invoice = Invoice.objects.create(order=self.order)

    def test_invoice_serializer_order(self):
        serializer = InvoiceSerializer(instance=self.invoice)
        self.assertEqual(serializer.data['order']['id'], self.order.id)

    def test_invoice_serializer_customer(self):
        serializer = InvoiceSerializer(instance=self.invoice)
        self.assertEqual(serializer.data['customer']['id'], self.customer.id)

    def test_invoice_serializer_fields(self):
        expected_fields = ['invoice_id', 'order', 'customer', 'issued_at']
        serializer = InvoiceSerializer(instance=self.invoice)
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))


