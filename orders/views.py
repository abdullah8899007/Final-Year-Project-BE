from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from django.db.models import Prefetch, Sum
from accounts.permissions import IsStaff
from menu.serializers import ItemSerializer, NewItemSerializer
from .models import  *
from .serializers import OrdersSerializer, InvoiceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = OrdersSerializer

    def get_queryset(self):
        return Orders.objects.all()

    @action(detail=False, methods=['get'])
    def all_orders(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class InvoiceViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
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


class AnalyticsViewSet(ViewSet):
    @action(detail=False, methods=['get'], url_path='categories-sales')
    def categories_sales(self, request):
        # Aggregate total items sold for each category
        category_sales = (
            Category.objects.annotate(total_sold=Sum('item__sold'))
            .filter(total_sold__isnull=False)  # Exclude categories with no sold items
            .order_by('-total_sold')
        )

        if not category_sales.exists():
            return Response({"detail": "No sales data available."}, status=404)

        total_sales = sum(category.total_sold for category in category_sales)

        data = [
            {
                "category_name": category.name,
                "total_sold": category.total_sold,
                "percentage": round((category.total_sold / total_sales) * 100, 2),
                "image": category.image
            }
            for category in category_sales
        ]

        return Response(data)
