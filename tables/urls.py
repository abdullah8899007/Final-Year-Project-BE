from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'tables'

urlpatterns = [
    # path('reservations/', views.ReservationView.as_view(), name='reservations'),
    # path('reservation/<int:id>/', views.ReservationView.as_view(), name='reservation'),
]



router = DefaultRouter()
router.register('tables', views.TableViewSet, basename='tables')
router.register('reservations', views.ReservationViewSet, basename='reservations')

urlpatterns += router.urls