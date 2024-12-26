from django.shortcuts import render
from rest_framework.decorators import APIView, api_view, action
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

    @action(detail=False, methods=['get'], url_path='all_items')
    def get_all_items(self, request):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

class NewCategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsStaff]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()