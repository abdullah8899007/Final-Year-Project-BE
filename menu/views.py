from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from django.db.models import Count, Sum, Avg
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from accounts.permissions import IsStaff


from .serializers import *
from .models import *
# Create your views here.
from django.db.models import F, FloatField, ExpressionWrapper


class CategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsStaff]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     main_data = serializer.data

    #     total_items = Category.objects.aggregate(total_count=Sum("count"))["total_count"]

    #     comparison_data = {}

    #     if total_items:
    #         categories = Category.objects.annotate(category_percentage=ExpressionWrapper(F('count') * 100.0 / total_items, output_field=FloatField()))
    #         category_percentage_list = []

    #         for category in categories:
    #             category_percentage_list.append({category.name: category.category_percentage})

    #         # Construct the comparison data dictionary
    #         comparison_data["comparison"] = category_percentage_list

    #     # Combine main data and comparison data into a single dictionary
    #     response_data = {"main_data": main_data, **comparison_data}

    #     return Response(response_data)



class DealViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsStaff]
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())

    #     # Serialize the items
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = serializer.data

    #     # Calculate the count of items per category
    #     items_per_category = Item.objects.values('category__name').annotate(num_items=Count('id'))

    #     for category_data in items_per_category:
    #         category_name = category_data['category__name']
    #         num_items = category_data['num_items']
    #         data.append({category_name: num_items})

    #     return Response(data, status=status.HTTP_200_OK)