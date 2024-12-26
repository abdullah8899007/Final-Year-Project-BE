from django.urls import path

from menu.views import ItemViewSet
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'orders' 


router = DefaultRouter()

router.register('orders', OrderViewSet, basename='orders')
router.register('invoices', InvoiceViewSet, basename='invoices')
router.register('latest_orderdetail',OrderItemSet,basename='latest_orderdetail')
router.register('analytics', AnalyticsViewSet, basename='analytics')


urlpatterns = [
    
] + router.urls
