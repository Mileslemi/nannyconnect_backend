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
        
class UserSerializer(UserSerializer):
    location = AddressSerializer(read_only=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email','first_name','last_name','phone_number','location', 'is_staff','user_type','image')
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        if representation['user_type'] == 'nanny':
            if Nanny.objects.filter(user=representation['id']).exists():
                representation['nanny'] = MiniNannySerializer(Nanny.objects.get(user=representation['id'])).data
        return representation 
    
class MiniUserSerializer(ModelSerializer):
    location = AddressSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email','first_name','last_name','phone_number','location', 'image')
class NannySerializer(ModelSerializer):
    user = MiniUserSerializer(read_only=True)
    class Meta:
        model = Nanny
        fields = '__all__'

class MiniNannySerializer(ModelSerializer):
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
    nanny = NannySerializer(read_only=True)
    user = MiniUserSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"
        

