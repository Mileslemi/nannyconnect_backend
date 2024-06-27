from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Booking)
admin.site.register(Nanny)
admin.site.register(Notifications)
admin.site.register(Chats)
admin.site.register(Complaints)
admin.site.register(NannyForms)
