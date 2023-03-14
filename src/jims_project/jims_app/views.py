from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from jims_app.forms import SignUpForm

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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('userEmail')
            user = authenticate(username = username, password = raw_password, email = email)
            login(request,user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})