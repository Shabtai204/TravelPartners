from django.contrib import admin
from .models import Trip, Type, Message, User

# Register your models here.

admin.site.register(User)
admin.site.register(Trip)
admin.site.register(Type)
admin.site.register(Message)
