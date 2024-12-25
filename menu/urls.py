from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'menu'


router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('items', views.ItemViewSet, basename='items')
router.register('deals', views.DealViewSet, basename='deals')

urlpatterns = [
    path('', include(router.urls)),
]