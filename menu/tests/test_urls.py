from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from menu.models import Category, Item, Deal
from menu.views import CategoryViewSet, ItemViewSet, DealViewSet
from custom_user.models import User
from datetime import datetime, timedelta
import json
from django.core.files import File

class AuthenticatedAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class CategoryAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        self.url = reverse('menu:categories-list')

    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)
    
    def test_create_category(self):
        data = {'name': 'Test Category', 'image':"this is image code"}
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name='Test Category').exists())
    
    def test_retrieve_category(self):
        url = reverse('menu:categories-detail', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['name'], 'Category 1')

    def test_update_category(self):
        url = reverse('menu:categories-detail', args=[self.category1.id])
        data = {'name': 'Updated Category'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.get(id=self.category1.id).name, 'Updated Category')

    def test_delete_category(self):
        url = reverse('menu:categories-detail', args=[self.category1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)


class ItemAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='Category 1')
        self.item1 = Item.objects.create(name='Item 1', description='Description 1', category=self.category, price=10)
        self.item2 = Item.objects.create(name='Item 2', description='Description 2', category=self.category, price=20)
        self.url = reverse('menu:items-list')

    def test_get_items(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_create_item(self):
        data = {'name': 'Test Item',"description":"This is test","categoryId":1, "price":20 ,'image': "This is image code"}
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Item.objects.filter(name='Test Item').exists())
    
    def test_retrieve_item(self):
        url = reverse('menu:items-detail', args=[self.item1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['name'], 'Item 1')

    def test_update_item(self):
        url = reverse('menu:items-detail', args=[self.item1.id])
        data = {'name': 'Updated Item'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(id=self.item1.id).name, 'Updated Item')

    def test_delete_item(self):
        url = reverse('menu:items-detail', args=[self.item1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 1)

class DealAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='Category 1')
        self.deal1 = Deal.objects.create(name='Deal 1', starting_date='2024-02-21', end_date='2024-02-28', items=[], discounted_price=899.99)
        self.deal2 = Deal.objects.create(name='Deal 2', starting_date='2024-02-21', end_date='2024-02-28', items=[], discounted_price=799.99)
        self.url = reverse('menu:deals-list')

    def test_get_deals(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)

    def test_create_deal(self):
        data = {'name': 'Test Deal',"starting_date":'2024-02-21', "end_date":'2024-02-28',"items":json.dumps({"burger": 1}),"discounted_price":100, "status":True ,'image':"this is image code"}
        response = self.client.post(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Deal.objects.filter(name='Test Deal').exists())
    
    def test_retrieve_deal(self):
        url = reverse('menu:deals-detail', args=[self.deal1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())
        self.assertEqual(response.json()['data']['name'], 'Deal 1')

    def test_update_deal(self):
        url = reverse('menu:deals-detail', args=[self.deal1.id])
        data = {'name': 'Updated deal'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Deal.objects.get(id=self.deal1.id).name, 'Updated deal')

    def test_delete_deal(self):
        url = reverse('menu:deals-detail', args=[self.deal1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Deal.objects.count(), 1)
