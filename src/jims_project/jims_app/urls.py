from django.urls import path
from . import views

# Add your URL paths that belong to the jims_app here
urlpatterns = [
        path('', views.login, name = 'login')
]