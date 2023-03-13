from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login(request):
    """
    login function that renders the login.html page when it is called
    """

    return render(request, 'login.html')