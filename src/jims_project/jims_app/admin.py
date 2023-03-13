from django.contrib import admin
from .models import login

# Register your models here.

# Register the 'login' model with the Django admin site to enable admin management of the 'login' model data
admin.site.register(login)

