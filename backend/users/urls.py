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
  path('add_review/', ReviewNanny.as_view(), name="add review"),
  path('complaints/', ComplaintsList.as_view(), name="complaints list"),
  path('complaints/<int:pk>/', ComplaintDetail.as_view(), name="complaint detail"),
  path('upload_nanny_form/', NannyFormsUploading.as_view(), name="upload nanny form"),
  path('notifications/', NotificationsList.as_view(), name="notifications list"),
  path('notifications/<int:pk>/', NotificationsDetail.as_view(), name="notification detail"),
  path('filter_notifications/', FilterNotifications.as_view(), name="filter notifacions"),
  path('chats/', ChatsList.as_view(), name="chats"),
  path('chats/<int:pk>/', ChatDetail.as_view(), name="chat detail"),
  path('get_chats/', getChats, name="get chats"),
  path('unread_notifications/', unReadNotificationsCount, name="unread notifications"),
  path('update_notifications/', updateAsRead, name="update notifications as read"),
  path('<str:username>/', UserDetail.as_view(), name="user detail"),
]