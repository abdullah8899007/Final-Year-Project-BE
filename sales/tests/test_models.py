from django.test import TestCase
from .models import MainBalance,PaymentHistory
from orders.models import Orders
from datetime import datetime


class MainBalanceTestCase(TestCase):
    def setUp(self):
        Orders.objects.create(total_price=100)
        Orders.objects.create(total_price=200)
        Orders.objects.create(total_price=300)

    def test_calculate_total_price(self):
        main_balance = MainBalance.objects.create()

        total_price = main_balance.calculate_total_price()

        expected_total_price = 100 + 200 + 300
        self.assertEqual(total_price, expected_total_price)

        main_balance.refresh_from_db()

        self.assertEqual(main_balance.total_price, expected_total_price)
        
        
        


class PaymentHistoryTestCase(TestCase):
    def setUp(self):
        self.customer_name = CustomersModel.objects.create(name="Abdullah Khan")
        self.payment_history = PaymentHistory.objects.create(
            customer_name=self.customer_name,
            data_issued=datetime.now(),
            payment_type='CASH',
            payment_status='PAID'
        )

    def test_payment_history_creation(self):
        payment_history = PaymentHistory.objects.get(customer_name=self.customer_name)
        self.assertEqual(payment_history.customer_name, self.customer_name)
        self.assertTrue(payment_history.data_issued)
        self.assertEqual(payment_history.payment_type, 'CASH')
        self.assertEqual(payment_history.payment_status, 'PAID')

