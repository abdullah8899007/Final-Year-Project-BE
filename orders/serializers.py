from rest_framework import serializers
from .models import *
from customers.models import CustomersModel
from customers.serializers import CustomerSerializer


class OrdersSerializer(serializers.ModelSerializer):
    customerId = serializers.PrimaryKeyRelatedField(queryset=CustomersModel.objects.all(), source='customer')
    name = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ['id', 'customerId', 'name', 'items', 'deals', 'status', 'orderType', 'total', 'created_at']

    def get_name(self, obj):
        return obj.customer.name


class InvoiceSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    order = OrdersSerializer(read_only=True)
    customer = CustomerSerializer(source='order.customer', read_only=True)

    class Meta:
        model = Invoice
        fields = ['invoice_id', 'order_id', 'order','customer', 'issued_at']
        read_only_fields = ['order','customer'] 

        
    def create(self, validated_data):
        order_id = validated_data.pop('order_id')
        try:
            order = Orders.objects.select_related('customer').get(pk=order_id)
            invoice = Invoice.objects.create(order=order, **validated_data)
            return invoice
        except Orders.DoesNotExist:
            raise serializers.ValidationError({"error": "Order does not exist"})

class NewInvoiceSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    invoice_id = serializers.IntegerField(read_only=True)
    order = OrdersSerializer(read_only=True)
    customer = CustomerSerializer(source='order.customer', read_only=True)

    class Meta:
        model = Invoice
        fields = ['invoice_id', 'order_id', 'order', 'customer', 'issued_at']
        read_only_fields = ['order', 'customer']

    def create(self, validated_data):
        order_id = validated_data.pop('order_id')
        try:
            order = Orders.objects.select_related('customer').get(pk=order_id)
            invoice = Invoice.objects.create(order=order, **validated_data)
            return invoice
        except Orders.DoesNotExist:
            raise serializers.ValidationError({"error": "Order does not exist"})