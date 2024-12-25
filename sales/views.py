import calendar
from datetime import datetime, timedelta
from django.db.models.functions import ExtractWeekDay, ExtractIsoWeekDay

from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsStaff
from orders.models import Orders, Invoice
from orders.serializers import OrdersSerializer, NewInvoiceSerializer
from customers.models import CustomersModel
from django.db.models import Sum


class MainBalanceViewset(viewsets.ViewSet):
    # permission_classes = [IsStaff]
    serializer_class = OrdersSerializer

    def list(self, request):
        MainBalance = Orders.objects.aggregate(total_price_sum=Sum('total'))['total_price_sum'] or 0
        return Response({'MainBalance': MainBalance})


class PaymentHistoryViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsStaff]

    serializer_class = OrdersSerializer

    def get_queryset(self):
        queryset = Orders.objects.filter(status='Completed').values('customer__name', 'total', 'orderType', 'status',
                                                                    'created_at')
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        data = list(queryset)
        return Response(data)


class InvoiceSentViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsStaff]
    
    serializer_class = OrdersSerializer
    
    
    def get_queryset(self):
        return Orders.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset().values('customer__name', 'total', 'created_at')
        data = list(queryset)
        return Response(data)

class NewInvoiceSentViewSet(viewsets.ModelViewSet):
    serializer_class = NewInvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.select_related('order__customer')

    def list(self, request):
        queryset = self.get_queryset()
        serialized_data = NewInvoiceSerializer(queryset, many=True).data

        # Reshape the data to include only required fields
        simplified_data = [
            {
                "invoice_id": item["invoice_id"],
                "order_id": item["order_id"],
                "customer_name": item["customer"]["name"],
                "total": item["order"]["total"],
                "issued_at": item["issued_at"],
            }
            for item in serialized_data
        ]

        return Response({
            "success": True,
            "status": 200,
            "data": simplified_data
        })


class MonthlySalesViewSet(viewsets.ViewSet):
    def list(self, request):
        sales_data = (
            Orders.objects
            .filter(created_at__year=datetime.now().year)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total_sales=Sum('total'))
            .order_by('month')
        )

        monthly_sales = {month: 0 for month in calendar.month_name[1:]}

        for entry in sales_data:
            month_name = entry['month'].strftime('%B')
            monthly_sales[month_name] = entry['total_sales']

        data = [{'month': month, 'total_sales': total_sales} for month, total_sales in monthly_sales.items()]

        return Response(data)


class WeeklySalesViewSet(viewsets.ViewSet):
    def list(self, request):
        now = timezone.localtime(timezone.now())

        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

        sales_data = (
            Orders.objects
            .filter(created_at__range=[start_of_week, end_of_week])
            .annotate(day_of_week=ExtractIsoWeekDay('created_at'))  # Monday=1, Sunday=7
            .values('day_of_week')
            .annotate(total_sales=Sum('total'))
            .order_by('day_of_week')
        )

        weekly_sales = {day: 0 for day in calendar.day_name}

        for entry in sales_data:
            sql_weekday = entry['day_of_week']
            day_name = calendar.day_name[sql_weekday - 1]
            weekly_sales[day_name] = entry['total_sales']

        data = [{'day': day, 'total_sales': total_sales} for day, total_sales in weekly_sales.items()]
        return Response({"success": True, "status": 200, "data": data})
