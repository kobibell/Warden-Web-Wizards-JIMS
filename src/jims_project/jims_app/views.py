from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.middleware import csrf

from django.contrib.auth import get_user_model

User = get_user_model()


from .models import Accounts
from .models import TransactionDetails

# Create your views here.

def user_login(request):
    """
    Authenticates a user using Django's built-in authentication system.

    If the user is authenticated, logs them in and redirects them to the appropriate page.
    If the user is not authenticated, displays an error message and logs the failed login attempt.

    Args:
        request (HttpRequest): The HTTP request object representing the current request.

    Returns:
        HttpResponse: Renders the login page
    """
    if request.method == 'POST':
        # Get the username and password from the request POST data
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using Django's built-in authentication system
        user = authenticate(request, username=user_name, password=password)

        # If the user is authenticated, log them in and redirect to the appropriate page
        if user is not None:
            auth_login(request, user)

            #If the user is a superuser redirect them to the django admin page otherwise redirect them to the home page

            #!TODO : Redirect for each user type 
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('/home_page/')
            
         # If the user is not authenticated display an error message and log the failed login attempt (in the Djano Admin Page)
        else:
            messages.error(request, 'Invalid username or password')
            print(f"Failed login attempt: username={user_name}, password={password}") 

    # Render the login page with a CSRF token for security
    return render(request, 'login.html', {'csrf_token': csrf.get_token(request)})

def create_user(request):
    """
    Creates a new user using the CustomUserManager and saves them to the database.

    Args:
        request (HttpRequest): The HTTP request object representing the current request.
    """

    # If the request method is post
    if request.method == 'POST':

        # Get the form data from the request POST data
        email = request.POST['email']
        user_name = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        position = request.POST['position']

        # Create the user using your CustomUserManager
        user = User.objects.create_user(email=email, user_name=user_name, password=password, position = position, first_name = first_name, last_name = last_name)

        # Return a success response
        #!TODO Finish create user success
        return render(request, 'create_user_success.html', {'user': user})

    #If the request is GET render the HTML form create_user.html
    else:
        return render(request, 'create_user.html')

@login_required
def home_page(request):
    return render(request, 'home_page.html')

@login_required
def accounts_home(request):
    return render(request, 'accounts_home.html')  

@login_required
def accounts_transaction_details(request):
    return render(request, 'accounts_search_number.html')  

@login_required
def accounts_search_name(request):
    return render(request, 'accounts_search_name.html')

@login_required
def get_all_accounts(request):
    accounts = Accounts.objects.all()
    context = {'accounts': accounts}
    return render(request, 'account_list.html', context)

def get_all_transaction_details(request):
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