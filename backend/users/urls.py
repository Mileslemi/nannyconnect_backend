from django.urls import path
from .views import *

urlpatterns = [
  path('', UsersList.as_view(), name="users list"),
  path('bookings/', BookingList.as_view(), name="bookings"),
  path('bookings/<int:pk>/',BookingDetail.as_view(), name="booking detail"),
  path('<str:username>/', UserDetail.as_view(), name="user detail")
]