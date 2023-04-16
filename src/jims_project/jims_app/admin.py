from django.contrib import admin
from .models import *

# Register your models here.

# Register the 'login' model with the Django admin site to enable admin management of the 'login' model data
admin.site.register(Officer)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass