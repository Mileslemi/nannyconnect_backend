
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Booking
from .serializers import *

# Create your views here.
# create an authenticated view to fetch all user detials by email
class UsersList(APIView):
    serializer_class = UserSerializer
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    serializer_class = UserSerializer
    
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
            
    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()          
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingList(APIView):
    serializer_class = BookingSerializer
    def get(self, request):
        booking_items = Booking.objects.all()
        serializer = BookingSerializer(booking_items, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class BookingDetail(APIView):
    serializer_class = BookingSerializer
    
    def get_object(self, pk):
        try:
            return Booking.objects.get(id=pk)
        except Booking.DoesNotExist:
            raise Http404
            
    def get(self, request, pk):
        booking_item = self.get_object(pk)
        serializer = BookingSerializer(booking_item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        booking_item = self.get_object(pk)
        
        serializer = BookingSerializer(booking_item, data=request.data)
        if serializer.is_valid():
            serializer.save()          
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        # when you delete, it is auto-deleted in the m2m relation table, very nice
        booking_item = self.get_object(pk)
        booking_item.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)