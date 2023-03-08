from django.urls import path
from . import views


urlpatterns = [
    
    # User comes to specified url and what ever function or class is declared will be run for the user. 
    path('', views.index, name ='index')
]