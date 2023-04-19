from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.middleware import csrf
from .forms import InmateForm

from django.contrib.auth import get_user_model

User = get_user_model()


from .models import Accounts, CustomUser
from .models import TransactionDetails

from .forms import AddMoneyForm
from .forms import WithdrawMoneyForm

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
                return render(request, 'home_page.html')
            
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
    context = {
        'user': request.user,
    }
    return render(request, 'home_page.html', context)



@login_required
def accounts_home(request):
    context = {
        'user_position': request.user.position,
    }
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
        filter_by = request.POST.get('search_num')
        if filter_by:
            transaction_details = TransactionDetails.objects.filter(account_number=filter_by)
            context = {'transaction_details': transaction_details}
            return render(request, 'transaction_details_list.html', context)

    return render(request, 'transaction_details_list.html')

def add_money(request):  
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            try:
             account = Accounts.objects.get(account_number=form.cleaned_data['account_number'])
            except Accounts.DoesNotExist:
                account = None

            if(account):
                account.balance = account.balance + form.cleaned_data['amount']
                transaction = TransactionDetails.objects.create(account_number=account, transaction_type='D', transaction_amount=form.cleaned_data['amount'], transaction_date=timezone.now())
                account.save()
                transaction.save()
                return render(request, 'add_money.html', {'message': 'Money added successfully'})
            else:
                return render(request, 'add_money.html', {'message': 'Account does not exist'})
    else:
        form = AddMoneyForm()
    return render(request, 'add_money.html', {'form': form})

def withdraw_money(request):  
    if request.method == 'POST':
        form = WithdrawMoneyForm(request.POST)
        if form.is_valid():
            try:
             account = Accounts.objects.get(account_number=form.cleaned_data['account_number'])
            except Accounts.DoesNotExist:
                account = None

            if(account):
                account.balance = account.balance - form.cleaned_data['amount']

                if (account.balance < 0):
                    return render(request, 'withdraw_money.html', {'message': 'Insufficient funds'})
                else:
                    transaction = TransactionDetails.objects.create(account_number_id=account.account_number, transaction_type='W', transaction_amount=form.cleaned_data['amount'], transaction_date=timezone.now())
                    account.save()
                    transaction.save()
                    return render(request, 'withdraw_money.html', {'message': 'Money withdrawn successfully'})
            else:
                return render(request, 'withdraw_money.html', {'message': 'Account does not exist'})
    else:
        form = WithdrawMoneyForm()
    return render(request, 'withdraw_money.html', {'form': form})
    
  
def add_inmate(request):
    if request.method == 'POST':
        form = InmateForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'inmate_confirmation.html')
    else:
        form = InmateForm()
    return render(request, 'add_inmate.html', {'form': form})


def create_user_success(request):
    return render(request, 'create_user_success.html')

def inventory(request):
    return render(request, 'inventory.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

