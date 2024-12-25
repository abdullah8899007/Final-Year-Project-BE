from rest_framework import serializers
from .models import *
from customers.models import CustomersModel

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class ReservationsSerializer(serializers.ModelSerializer):
    table_id = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), source='table')
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomersModel.objects.all(), source='user')
    class Meta:
        model = Reservation
        fields = ['id','user_id','table_id','status','booking_time']