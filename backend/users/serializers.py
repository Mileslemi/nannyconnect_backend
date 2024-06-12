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
    address = AddressSerializer(read_only=True)
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id','email','first_name','last_name','phone_number','address', 'is_staff','user_type')
        
class NannySerializer(ModelSerializer):
    class Meta:
        model = Nanny
        fields = '__all__'
        
class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
    # def to_representation(self, instance):
    #     representation =  super().to_representation(instance)
    #     return representation
        

