from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'main-balance', MainBalanceViewset,basename='main-balance')
router.register(r'payment-history',PaymentHistoryViewSet,basename='payment-history')
router.register(r'invoice-sent',InvoiceSentViewSet,basename='invoice-sent')
router.register(r'monthly-sales', MonthlySalesViewSet, basename='monthly-sales')
router.register(r'weekly-sales', WeeklySalesViewSet, basename='weekly-sales')
router.register(r'invoices', NewInvoiceSentViewSet, basename='invoice')


urlpatterns = [
    path('', include(router.urls)),
]