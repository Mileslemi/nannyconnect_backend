from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from .models import *


User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        # fields = ['id','email','name','phone_number','address']
        fields = '__all__'


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class MiniUserSerializer(ModelSerializer):
    location = AddressSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email','first_name','last_name','phone_number','location', 'image', 'suspended')

class MiniMiniUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','phone_number','image', 'suspended')


class ReviewReadSerializer(ModelSerializer):
    reviewer = MiniUserSerializer(read_only=True)
    class Meta:
        model = Reviews
        fields = "__all__"

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
        
class UserSerializer(UserSerializer):
    location = AddressSerializer(read_only=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email','first_name','last_name','phone_number','location', 'is_staff','user_type','image', 'suspended')
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        if representation['user_type'] == 'nanny':
            if Nanny.objects.filter(user=representation['id']).exists():
                representation['nanny'] = MiniNannySerializer(Nanny.objects.get(user=representation['id'])).data
        return representation 
    
class ReviewReadSerializer(ModelSerializer):
    reviewer = MiniUserSerializer(read_only=True)
    class Meta:
        model = Reviews
        fields = "__all__"

class NannyFormsSerializer(ModelSerializer):
    class Meta:
        model = NannyForms
        fields = "__all__"    

class NannySerializer(ModelSerializer):
    class Meta:
        model = Nanny
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # user = User.objects.get(id=representation['user'])
        representation['user'] = MiniUserSerializer(instance.user, read_only=True).data
        # docs
        if instance.docs != None:
            representation['docs'] = NannyFormsSerializer(instance.docs, many=False, read_only=True).data
        # reviews
        reviews_listing = []
        
        for review in instance.reviews.all():
            seria_lizer = ReviewReadSerializer(review, many=False, read_only=True)
            reviews_listing.append(seria_lizer.data)
        representation['reviews'] = reviews_listing
        return representation

class MiniNannySerializer(ModelSerializer):
    user = MiniUserSerializer(read_only=True)
    class Meta:
        model = Nanny
        fields = '__all__'
        
class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        user = User.objects.get(id=representation['user'])
        representation['user'] = MiniUserSerializer(user, read_only=True).data
        nanny = Nanny.objects.get(id=representation['nanny'])
        representation['nanny'] = NannySerializer(nanny, read_only=True).data
        return representation
class ExtBookingSerializer(ModelSerializer):
    nanny = MiniNannySerializer(read_only=True)
    user = MiniUserSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"

class ComplaintsSerializer(ModelSerializer):
    class Meta:
        model = Complaints
        fields = "__all__"
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
    
        representation['booking'] = ExtBookingSerializer(instance.booking, many=False, read_only=True).data
        return representation
        
class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sender'] = MiniMiniUserSerializer(instance.sender, many=False, read_only=True).data
        representation['receiver'] = MiniMiniUserSerializer(instance.receiver, many=False, read_only=True).data
        
        return representation

class ChatsSerializer(ModelSerializer):
    class Meta:
        model = Chats
        fields = "__all__"
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['party_a'] = MiniMiniUserSerializer(instance.party_a, many=False, read_only=True).data
        representation['party_b'] = MiniMiniUserSerializer(instance.party_b, many=False, read_only=True).data
        
        # notifications
        notifications = []
        
        for n in instance.notifications.all():
            seria_lizer = NotificationSerializer(n, many=False, read_only=True)
            notifications.append(seria_lizer.data)
        representation['notifications'] = notifications
        return representation