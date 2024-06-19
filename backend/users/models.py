from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

class Address(models.Model):
    address = models.CharField(max_length=64,null=True, blank=True)
    town = models.CharField(max_length=16,null=True, blank=True)
    county = models.CharField(max_length=16,null=True, blank=True)
    country = models.CharField(max_length=16, default="Kenya")
    
    def __str__(self) -> str:
        if self.address:
            return self.address 
        elif self.town:
            return self.town
        elif self.county:
            return self.county
        else:
            return self.country

class UserAccountManager(BaseUserManager):
    # create normal user
    def create_user(self, username, email, first_name, last_name, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError("Username must be provided")
        if not email:
            raise ValueError("Email must be provided")
        # will turn Mileslemi to mileslemi
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, **extra_fields)
        
        # hash password using inbuilt django fn
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    # create superuser
    def create_superuser(self, username, email, first_name, last_name, phone_number, password=None):
        if not username:
            raise ValueError("Username must be provided")
        if not email:
            raise ValueError("Email must be provided")
        # will turn Mileslemi to mileslemi
        email = self.normalize_email(email)
        user = self.model(username=username.lower(), email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, is_staff=True, is_superuser=True)
        
        # hash password using inbuilt django fn
        user.set_password(password)
        user.save()
        
        return user        

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r"^(?:[+0])[0-9]{9,16}$", message="Invalid Phone Number!")
    phone_number =models.CharField(validators=[phone_regex], max_length=15)
    date_created_gmt = models.DateTimeField(auto_now_add=True)
    date_modified_gmt =  models.DateTimeField(auto_now=True)
    location = models.OneToOneField(Address, blank=True, null=True, on_delete=models.PROTECT)
    image = models.ImageField(upload_to="images/")
    user_type_choices = {"nanny":"Nanny","family":"Family"}
    user_type = models.CharField(max_length=16, choices=user_type_choices, blank=True, null=True)
    
    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number', 'user_type','location']
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def get_short_name(self):
        return self.last_name
    
    def __str__(self):
        return self.username

class Nanny(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    availabity = models.BooleanField(default=False)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

class Booking(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.RESTRICT)
    nanny = models.ForeignKey(Nanny, related_name="nanny", on_delete=models.RESTRICT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    negotiated_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status_choice = {"pending":"Pending", "confirmed":"Confirmed","rejected":"Rejected" ,"cancelled":"Cancelled", "done":"Done"}
    status = models.CharField(max_length=16, choices=status_choice, default="pending")
    details = models.TextField(null=True, blank=True)
    