from django.test import TestCase
from orders.models import Orders, Invoice
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from customers.models import CustomersModel



class OrdersModelTestCase(TestCase):
    def test_create_orders_instance(self):
        self.customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders.objects.create(
            customer=self.customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType="Type1",
            total=100
        )
        self.assertEqual(order.customer.name, "Test Customer")
        self.assertEqual(order.status, "Enqueue")

    def test_create_invoice_instance(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders.objects.create(
            customer=customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType ="Type1",
            total =100
        )
        invoice = Invoice.objects.create(order=order)
        self.assertEqual(invoice.order, order)

    def test_order_status_update(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders.objects.create(
            customer=customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType ="Type1",
            total = 100
        )
        order.status = "Ready"
        order.save()
        self.assertEqual(order.status, "Ready")


    def test_order_items_deals_empty(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders.objects.create(
            customer=customer,
            items={"item1": 2}, 
            deals={}, 
            status="Enqueue",
            orderType="Dinner",
            total=0
        )
        self.assertDictEqual(order.items, {"item1": 2})
        self.assertDictEqual(order.deals, {})


    def test_order_status_choices(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders(
            customer=customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="InvalidStatus",  
            orderType ="Dinner",
            total =100
        )
        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_order_invalid_quantity(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders(
            customer=customer,
            items={"item1": -1},
            deals={"deal1": 2},
            status="InvalidStatus",  
            orderType ="Dinner",
            total =100
        )
        with self.assertRaises(ValidationError):
            order.full_clean()


    def test_order_invalid_total (self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders(
            customer=customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="InvalidStatus",  
            orderType ="Dinner",
            total =-100
        )
        with self.assertRaises(ValidationError):
            order.full_clean()


    def test_order_invalid_orderType (self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders(
            customer=customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="InvalidStatus",  
            orderType ="Brunch",
            total =100
        )
        with self.assertRaises(ValidationError):
            order.full_clean()


class InvoiceModelTestCase(TestCase):
    def test_invoice_unique_invoice_id(self):
        customer = CustomersModel.objects.create(name="Test Customer", phone="1234567890", email="test@example.com", address="123 Test St")
        order = Orders.objects.create(
            customer=customer,
            items={"item1": 1},
            deals={"deal1": 2},
            status="Enqueue",
            orderType ="Dinner",
            total =100
        )
        Invoice.objects.create(order=order, invoice_id=1)
        with self.assertRaises(IntegrityError):
            Invoice.objects.create(order=order, invoice_id=1)




