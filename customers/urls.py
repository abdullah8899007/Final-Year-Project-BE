
from customers.views import CustomerViewSet
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('customer', CustomerViewSet, basename='customer')
router.register('create_customer', NewCustomerViewSet, basename='create_customer')


urlpatterns = [
    
    
] + router.urls
