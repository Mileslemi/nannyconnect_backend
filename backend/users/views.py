import datetime

from django.http import Http404, HttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from dateutil.parser import parse


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
        print(request.data)
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

class FilterBookings(APIView):
    serializer_class = ExtBookingSerializer
    
    def post(self, request):
        is_nanny = request.data.get("is_nanny", None)
        id = request.data.get("id", None)
        pending = request.data.get("pending", None)
        
        
        if id:
            if is_nanny:
                if pending:
                    booking_items = Booking.objects.filter(nanny=id, status='pending')
                    serializer = ExtBookingSerializer(booking_items, many=True)
                    return Response(serializer.data)
                else:
                    booking_items = Booking.objects.filter(nanny=id)
                    serializer = ExtBookingSerializer(booking_items, many=True)
                    return Response(serializer.data)
            else:
                # is family 
                booking_items = Booking.objects.filter(user=id)
                serializer = ExtBookingSerializer(booking_items, many=True)
                return Response(serializer.data)
                
        return Response([])
    
class AddressList(APIView):
    serializer_class = AddressSerializer
    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class AddressDetail(APIView):
    serializer_class = AddressSerializer
    
    def get_object(self, pk):
        try:
            return Address.objects.get(id=pk)
        except Address.DoesNotExist:
            raise Http404
            
    def get(self, request, pk):
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)
    
    def put(self, request, pk):
        address = self.get_object(pk)
        
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()          
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NannyList(APIView):
    serializer_class = NannySerializer
    def get(self, request):
        nannies = Nanny.objects.all()
        serializer = NannySerializer(nannies, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = NannySerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class NannyDetail(APIView):
    serializer_class = NannySerializer
    
    def get_object(self, pk):
        try:
            return Nanny.objects.get(id=pk)
        except Nanny.DoesNotExist:
            raise Http404
            
    def get(self, request, pk):
        nanny = self.get_object(pk)
        serializer = NannySerializer(nanny)
        return Response(serializer.data)
    
    def put(self, request, pk):
        nanny = self.get_object(pk)
        
        serializer = NannySerializer(nanny, data=request.data)
        if serializer.is_valid():
            serializer.save()          
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NannyFiltering(APIView):
    def post(self, request):
        start_time = request.data.get("start_time", None) # 2024-06-18T11:41:35.491391Z
        end_time = request.data.get("end_time", None)
        location = request.data.get("location", "")
        name = request.data.get("name", "")
        
        nannies = Nanny.objects.filter(Q(user__first_name__contains = name) | Q(user__last_name__contains = name), Q(user__location__address__contains = location) | Q(user__location__town__contains = location) | Q(user__location__county__contains = location))
        serializer = NannySerializer(nannies, many=True)
        
        filtered_nannies = serializer.data
        
        if start_time or end_time:          
            # check if nanny is confirmed booked at any point during that time
            final_nannies = []
            for nan in filtered_nannies:
                if start_time and end_time:                    
                    if not Booking.objects.filter(Q(start_time__lt = start_time) | Q (start_time__lt = end_time), Q(end_time__gt = start_time) | Q(end_time__gt = end_time), Q(status='pending') | Q(status='confirmed'), nanny=nan['id']).exists():
                        final_nannies.append(nan)
                        continue
                elif start_time:
                    if not Booking.objects.filter(Q(status='confirmed') | Q(status='pending'),start_time__lt = start_time, end_time__gt = start_time, nanny=nan['id']).exists():
                        final_nannies.append(nan)
                        continue
                else:
                    if not Booking.objects.filter(Q(status='confirmed') | Q(status='pending'), start_time__lt = end_time, end_time__gt = end_time, nanny=nan['id']).exists():
                        final_nannies.append(nan)
                        continue
            return Response(final_nannies)
        
        return Response(filtered_nannies)

@api_view(['POST'])
def checkBookingSlot(request):
    start_time = request.data.get("start_time", None) # 2024-06-18T11:41:35.491391Z
    end_time = request.data.get("end_time", None)
    nanny = request.data.get("nanny", None)
    if start_time and end_time and nanny:                    
        if Booking.objects.filter(Q(start_time__lt = start_time) | Q (start_time__lt = end_time), Q(end_time__gt = start_time) | Q(end_time__gt = end_time), Q(status='pending') | Q(status='confirmed'), nanny=nanny).exists():
            return Response(False)
    return Response(True)

class ReviewNanny(APIView):
    def post(self, request):
        reviewer = request.data.get("reviewer", None)
        review = request.data.get("review", None)
        rating = request.data.get("rating", None)
        nannyId = request.data.get("nanny_id", None)
        if reviewer and nannyId:
            serializer = ReviewSerializer(data={"reviewer":reviewer,"review":review,"rating":rating})       
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                saved_review = serializer.data 
                # link review with nanny
                nanny = Nanny.objects.get(id=nannyId)
                nanny.reviews.add(saved_review['id'])
                nanny.save()       
                return Response(saved_review)

class ComplaintsList(APIView):
    serializer_class = ComplaintsSerializer
    def get(self, request):
        complaints = Complaints.objects.all()
        serializer = ComplaintsSerializer(complaints, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = ComplaintsSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class ComplaintDetail(APIView):
    serializer_class = ComplaintsSerializer
    
    def get_object(self, pk):
        try:
            return Complaints.objects.get(id=pk)
        except Complaints.DoesNotExist:
            raise Http404
            
    def get(self, request, pk):
        complaint = self.get_object(pk)
        serializer = ComplaintsSerializer(complaint)
        return Response(serializer.data)
    
    def put(self, request, pk):
        complaint = self.get_object(pk)
        
        serializer = ComplaintsSerializer(complaint, data=request.data)
        if serializer.is_valid():
            serializer.save()          
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatsList(APIView):
    serializer_class = ChatsSerializer
    def get(self, request):
        chants = Chats.objects.all()
        serializer = ChatsSerializer(chants, many=True)
        return Response(serializer.data)

class ChatDetail(APIView):
    serializer_class = ChatsSerializer
    
    def get_object(self, pk):
        try:
            return Chats.objects.get(id=pk)
        except Chats.DoesNotExist:
            raise Http404
            
    def get(self, request, pk):
        chat = self.get_object(pk)
        serializer = ChatsSerializer(chat)
        return Response(serializer.data)
    
    def put(self, request, pk):
        chat = self.get_object(pk)
        
        serializer = ChatsSerializer(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()          
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NannyFormsUploading(APIView):
    serializer_class = NannyFormsSerializer
        
    def post(self, request):
        print(request.data)
        id_front = request.FILES["id_front"]
        id_back = request.FILES["id_back"]
        cert = request.FILES["cert"]
        nanny_id = request.data.get("nanny_id", None)
        
        if id_front and id_back and cert and nanny_id:
            serializer = NannyFormsSerializer(data={"id_front":id_front, "id_back":id_back, "cert":cert})
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                uploaded_form = serializer.data
                # update nanny docs
                nanny = Nanny.objects.get(id=nanny_id)
                nanny.docs = NannyForms.objects.get(id=uploaded_form['id'])
                nanny.save()                
                
                return Response(uploaded_form)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationsList(APIView):
    serializer_class = NotificationSerializer
    def get(self, request):
        notifications = Notifications.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        data = request.data
        serializer = NotificationSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            notif = serializer.data
            # update chat add this notif
            if Chats.objects.filter(Q(party_a=data['sender'],party_b=data['receiver'])|Q(party_a=data['receiver'],party_b=data['sender'])).exists():
                # chat exists, update 
                chat = Chats.objects.filter(Q(party_a=data['sender'],party_b=data['receiver'])|Q(party_a=data['receiver'],party_b=data['sender'])).first()
                chat.notifications.add(notif['id'])
                chat.save()
            else:
                chat_serializer = ChatsSerializer(data = {"party_a":data['sender'],"party_b":data['receiver'],"notifications":[notif['id']]})
                if chat_serializer.is_valid(raise_exception=True):                    
                    chat_serializer.save()                      
            return Response(notif)

class NotificationsDetail(APIView):
    serializer_class = NotificationSerializer
    
    def get_object(self, pk):
        try:
            return Notifications.objects.get(id=pk)
        except Notifications.DoesNotExist:
            raise Http404
            
    def get(self, request, pk):
        notif = self.get_object(pk)
        serializer = NotificationSerializer(notif)
        return Response(serializer.data)
    
    def put(self, request, pk):
        notif = self.get_object(pk)
        
        serializer = NotificationSerializer(notif, data=request.data)
        if serializer.is_valid():
            serializer.save()          
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# notification filtering -> filter by receiver and sender
class FilterNotifications(APIView):
    serializer_class = NotificationSerializer
    def post(self, request):
        receiver = request.data.get("receiver", None)
        sender = request.data.get("sender", None)
        if receiver and sender:
            notifications = Notifications.objects.filter(Q(sender=sender, receiver=receiver)|Q(sender=receiver, receiver=sender))
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def getChats(request):
    user_id = request.data.get("user_id", None)
    if user_id:
        chats = Chats.objects.filter(Q(party_a=user_id)|Q(party_b=user_id)).order_by('-date_modified_gmt')
        serializer = ChatsSerializer(chats, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# get all unread notifications of specific receiver, disticnt sender
@api_view(['POST'])
def unReadNotificationsCount(request):
    receiver = request.data.get("receiver", None)
    if receiver:
        count = Notifications.objects.filter(receiver=receiver, read=False).distinct('sender').count()
        return Response(count)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# update all notifications with certain sender and receiver, and where I'm receiver, as read
@api_view(['POST'])
def updateAsRead(request):
    receiver = request.data.get("receiver", None)
    sender = request.data.get("sender", None)
    if receiver and sender:
        Notifications.objects.filter(sender=sender, receiver=receiver, read=False).update(read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

