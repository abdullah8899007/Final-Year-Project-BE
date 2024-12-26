from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'menu'


router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('items', views.ItemViewSet, basename='items')
router.register('deals', views.DealViewSet, basename='deals')
router.register('all_categories', views.NewCategoryViewSet, basename='all_categories')

urlpatterns = [
    path('', include(router.urls)),
]