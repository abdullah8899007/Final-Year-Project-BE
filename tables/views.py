from django.shortcuts import render, get_object_or_404
from accounts.permissions import IsStaff
from rest_framework.decorators import APIView, api_view
from rest_framework import viewsets
from .serializers import *
from .models import *


# Create your views here.
class TableViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaff]

    serializer_class = TableSerializer
    queryset = Table.objects.all()


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaff]
    serializer_class = ReservationsSerializer
    queryset = Reservation.objects.all()
