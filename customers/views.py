from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CustomerSerializer
from .models import CustomersModel
from rest_framework import viewsets, status


class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = CustomerSerializer
    queryset = CustomersModel.objects.all()

class NewCustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = CustomerSerializer
    queryset = CustomersModel.objects.all()

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Get the latest customer based on created_at or id.
        """
        latest_customer = CustomersModel.objects.latest(
            'id')
        serializer = CustomerSerializer(latest_customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
