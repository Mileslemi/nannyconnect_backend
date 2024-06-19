from django.urls import path
from .views import *

urlpatterns = [
  path('', UsersList.as_view(), name="users list"),
  path('bookings/', BookingList.as_view(), name="bookings"),
  path('bookings/<int:pk>/',BookingDetail.as_view(), name="booking detail"),
  path('filter_bookings/', FilterBookings.as_view(), name="filter bookings"),
  path('address/', AddressList.as_view(), name="list addresses"),
  path('address/<int:pk>/', AddressDetail.as_view(), name="address detail"),
  path('nanny/', NannyList.as_view(), name="list nannies"),
  path('nanny/<int:pk>/', NannyDetail.as_view(), name="nanny detail"),
  path('filter_nannies/', NannyFiltering.as_view(),name="filter nannies"),
  path('check_booking/', checkBookingSlot, name="check booking"),
  path('<str:username>/', UserDetail.as_view(), name="user detail"),
]