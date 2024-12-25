from rest_framework import serializers
from .models import CustomersModel

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersModel
        fields = '__all__'
        