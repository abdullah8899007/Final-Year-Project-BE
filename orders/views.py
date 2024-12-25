from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from django.db.models import Prefetch
from accounts.permissions import IsStaff
from menu.serializers import ItemSerializer, NewItemSerializer
from .models import  *
from .serializers import OrdersSerializer, InvoiceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrdersSerializer

    def get_queryset(self):
        return Orders.objects.select_related('customer').all()


class InvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.select_related('order', 'order__customer').all()


class OrderItemSet(ViewSet):
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        latest_order = Orders.objects.last()
        if not latest_order:
            return Response({"detail": "No orders found."}, status=404)

        item_ids = [item.get('itemid') for item in latest_order.items]

        items = Item.objects.filter(id__in=item_ids)
        serialized_items = NewItemSerializer(items, many=True).data

        return Response({
            "items": serialized_items,
            "created_at": latest_order.created_at
        })


