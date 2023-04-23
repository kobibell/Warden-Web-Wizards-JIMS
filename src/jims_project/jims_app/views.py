from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.middleware import csrf
from .forms import *
from django.urls import reverse


from django.contrib.auth import get_user_model

User = get_user_model()


from .models import Accounts, CustomUser, InmateTraits
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
                return redirect('/home-page/')
            
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
                    transaction = TransactionDetails.objects.create(account_number=account, transaction_type='W', transaction_amount=form.cleaned_data['amount'], transaction_date=timezone.now())
                    account.save()
                    transaction.save()
                    return render(request, 'withdraw_money.html', {'message': 'Money withdrawn successfully'})
            else:
                return render(request, 'withdraw_money.html', {'message': 'Account does not exist'})
    else:
        form = WithdrawMoneyForm()
    return render(request, 'withdraw_money.html', {'form': form})
    
def view_inmate(request):
    return render(request, 'view_inmate.html')

def get_inmate_details(request):
    if request.method == 'POST':
        filter_by = request.POST.get('search_type')
        if filter_by == 'full_list':
            inmate_list = InmateTraits.objects.all()
            context = {'inmate_list': inmate_list}
            return render(request, 'inmate_result.html', context)
        
        if filter_by == 'by_first_name':
            search_var = request.POST.get('search-box')
            try:
                inmate = InmateTraits.objects.filter(first_name=search_var)
            except InmateTraits.DoesNotExist:
                return render(request, 'view_inmate.html')
            context= {'by_first_name': inmate}
            try: 
                return render(request, 'inmate_result.html', context)
            except InmateTraits.MultipleObjectsReturned:
                return render(request, 'view_inmate.html')
    
        if filter_by == 'by_last_name':
            search_var = request.POST.get('search-box')
            try:
                inmate = InmateTraits.objects.filter(last_name=search_var)
            except InmateTraits.DoesNotExist:
                return render(request, 'view_inmate.html')
            context= {'by_last_name': inmate}
            try: 
                return render(request, 'inmate_result.html', context)
            except InmateTraits.MultipleObjectsReturned:
                return render(request, 'view_inmate.html')
    
        if filter_by == 'by_id':
            search_var = request.POST.get('search-box')
            try:
                inmate = InmateTraits.objects.filter(id=search_var)
            except InmateTraits.DoesNotExist:
                None
            context= {'by_id': inmate}
            return render(request, 'inmate_result.html', context)
                
        return render(request, 'view_inmate.html')

from django.shortcuts import redirect

def add_inmate(request):
    
    # If the request method is POST process the form data
    if request.method == 'POST':

        # Create a form object with the POST data
        form = InmateForm(request.POST)

        # If the form is valid save the POST data to the session and redirect to the next page
        if form.is_valid():
            request.session['inmate_traits_data'] = request.POST
            return redirect('inmate_arrest_info')
        
    # If the request method is GET, render the form with info on the previous sesison
    else:
        form = InmateForm(initial=request.session.get('inmate_traits_data', None))
    
    # Render the add_inmate.html template with the form object as a context variable
    return render(request, 'add_inmate.html', {'inmate_traits_form': form})

def add_inmate_arrest_information(request):

    # If the request method is POST process the form data
    if request.method == 'POST':

        # Create a form object with the POST data
        form = InmateArrestingInfoForm(request.POST)
        
        # If the form is valid save the POST data to the session and redirect to the next page
        if form.is_valid():
            request.session['inmate_arrest_info_data'] = request.POST
            return redirect('inmate_health_sheet')
    # If the request method is GET, render a blank form
    else:
        form = InmateArrestingInfoForm(initial=request.session.get('inmate_arrest_info_data', None))


    # Render the inmate_arrest_info.html template with the form object as a context variable
    return render(request, 'inmate_arrest_info.html', {'inmate_arrest_info_form': form})

def add_inmate_health_sheet(request):

    # If the request method is POST process the form data
    if request.method == 'POST':

        # Create a form object with the POST data
        form = InmateHealthSheetForm(request.POST)
        
        # If the form is valid save the data from all three forms to the database and render a confirmation page
        if form.is_valid():

            # Get the inmate traits data from the session and create a form object with it
            inmate_form = InmateForm(request.session['inmate_traits_data'])

            #Check if its valid and save it
            if inmate_form.is_valid():
                inmate_form.save()

            # Get the arrest info data from the session and create a form object with it 
            arrest_info_form = InmateArrestingInfoForm(request.session['inmate_arrest_info_data'])

            # Check if its valid and save it
            if arrest_info_form.is_valid():
                arrest_info_form.save()

            # Save the current inmate health sheet form
            form.save()

            # Render confirmation page
            return render(request, 'inmate_confirmation.html')
    # If the request method is GET render a blank form
    else:
        form = InmateHealthSheetForm(initial=request.session.get('inmate_health_sheet_data', None))

    # Render the inmate_health_sheet.html template with the form object as a context variable
    return render(request, 'inmate_health_sheet.html', {'inmate_health_sheet_form': form})



def create_user_success(request):
    return render(request, 'create_user_success.html')

def inventory(request):
    return render(request, 'inventory.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout_success'))

def logout_success(request):
    return render(request, 'logout_success.html')
