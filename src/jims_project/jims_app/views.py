from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def login(request):
    """
    login function that renders the login.html page when it is called
    """

    if request.user.is_authenticated:
        if request.user.groups.filter(name='admins').exists():
            return redirect('/admin/')
        else:
            return redirect('/home_page/')
    else:
        return render(request, 'login.html')
    

def home_page(request):
    return render(request, 'home_page.html')

def accounts_home(request):
    return render(request, 'accounts_home.html')    