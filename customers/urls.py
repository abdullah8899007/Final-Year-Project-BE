
from customers.views import CustomerViewSet
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('customer', CustomerViewSet, basename='customer')


urlpatterns = [
    
    
] + router.urls
