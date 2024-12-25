from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from menu.models import Category, Item, Deal


class CategoryModelTestCase(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Electronics')
        self.assertEqual(category.name, 'Electronics')

    def test_category_str_method(self):
        category = Category.objects.create(name='Electronics')
        self.assertEqual(str(category), 'Electronics')


class ItemModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Electronics')

    def test_item_creation(self):
        item = Item.objects.create(
            name='Smartphone', description='Latest model', category=self.category, price=999)
        self.assertEqual(item.name, 'Smartphone')

    def test_item_str_method(self):
        item = Item.objects.create(
            name='Smartphone', description='Latest model', category=self.category, price=999)
        self.assertEqual(str(item), 'Smartphone')

    def test_item_stock_default_value(self):
        item = Item.objects.create(
            name='Smartphone', description='Latest model', category=self.category, price=999.99)
        self.assertEqual(item.stock, 10)

    def test_item_sold_default_value(self):
        item = Item.objects.create(
            name='Smartphone', description='Latest model', category=self.category, price=999.99)
        self.assertEqual(item.sold, 0)


class DealModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Electronics')

    def test_deal_creation(self):
        deal = Deal.objects.create(name='Special Deal', starting_date='2024-02-21',
                                    end_date='2024-02-28', items=[], discounted_price=899.99)
        self.assertEqual(deal.name, 'Special Deal')

    def test_deal_clean_method(self):
        with self.assertRaises(ValidationError):
            Deal.objects.create(name='Invalid Deal', starting_date='2024-02-28',
                                end_date='2024-02-21', items=[], discounted_price=899.99)

    def test_deal_save_method(self):
        deal = Deal(name='Special Deal', starting_date='2024-02-21',
                    end_date='2024-02-28', items=[], discounted_price=899.99)
        deal.save()
        self.assertIsNotNone(deal.id)

    def test_deal_str_method(self):
        deal = Deal.objects.create(name='Special Deal', starting_date='2024-02-21',
                                    end_date='2024-02-28', items=[], discounted_price=899.99)
        self.assertEqual(str(deal), 'Special Deal')
