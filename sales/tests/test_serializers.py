from django.test import TestCase
from .models import MainBalance,PaymentHistory
from .serializers import MainBalanceSerializer,PaymentHistorySerializer
        


class MainBalanceSerializerTestCase(TestCase):
    def test_get_total_price(self):
        main_balance = MainBalance.objects.create(total_price=600)  

        serializer = MainBalanceSerializer(instance=main_balance)

        expected_total_price = main_balance.calculate_total_price()
        self.assertEqual(serializer.data['total_price'], expected_total_price)
        


class PaymentHistorySerializerTestCase(TestCase):
    def setUp(self):
        self.payment_history_data = {
            'customer_name': 'Abdullah Khan',
            'data_issued': '2024-02-15T08:00:00Z',
            'payment_type': 'CASH',
            'payment_status': 'PAID'
        }
        self.payment_history = PaymentHistory.objects.create(**self.payment_history_data)

    def test_payment_history_serializer(self):
        serializer = PaymentHistorySerializer(instance=self.payment_history)
        self.assertDictEqual(serializer.data, self.payment_history_data)

