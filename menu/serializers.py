from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    categoryId = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')
    class Meta:
        model = Item
        # fields = ['id','name','description','image','price', 'category']
        fields = ['id','name','description','categoryId','image','price','stock']

class NewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name','image','price']

