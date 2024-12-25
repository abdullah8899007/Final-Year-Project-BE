
from .serializers import CustomerSerializer
from .models import CustomersModel
from rest_framework import viewsets
      


class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = CustomerSerializer
    queryset = CustomersModel.objects.all()
