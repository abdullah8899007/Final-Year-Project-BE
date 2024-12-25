from rest_framework.test import APIClient, APITestCase
from menu.serializers import CategorySerializer, ItemSerializer, DealSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from menu.models import Category, Item

class TestSerializers(APITestCase):
    
    def test_category_serializer(self):
        data = {
            "name":"TestName",
            "image":"This is test image code"
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    
    def test_item_serializer(self):
        category = Category.objects.create(name="Test") # to create category with id 1
        data = {'name': 'Test Name',
                'image': 'Test image code',
                "description":"test desc",
                "categoryId":1,
                "price":10
                }
        serializer = ItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())