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
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import *

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
                return redirect('home_page')
            
         # If the user is not authenticated display an error message and log the failed login attempt (in the Djano Admin Page)
        else:
            messages.error(request, 'Invalid username or password')
            print(f"Failed login attempt: username={user_name}, password={password}") 

    # Render the login page with a CSRF token for security
    return render(request, 'user/login.html', {'csrf_token': csrf.get_token(request)})

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

        existing_user = request.user.position
        print(existing_user)

        # Create the user using your CustomUserManager
        user = CustomUser.objects.create_user(email=email, user_name=user_name, password=password, position = position, first_name = first_name, last_name = last_name)

        user.save()

        # Return a success response
        #!TODO Finish create user success
        if existing_user == "Supervisor":
            return render(request, 'user/home_page.html')
        else:
            return render(request, "user/login.html")

    #If the request is GET render the HTML form create_user.html
    else:
        return render(request, 'user/create_user.html')

@login_required
def home_page(request):
    context = {
        'user': request.user,
    }
    return render(request, 'user/home_page.html', context)

@login_required
def accounts_home(request):
    """
    This function handles the deposit and withdrawal operations for a user's account. It processes the
    request, performs the required action based on the provided input, and returns the appropriate
    response to the user. It also displays the transaction history for the logged-in user.

    Args:
        request: The HTTP request object containing information about the current request.

    Returns:
        An HTTP response containing the accounts_home template rendered with the appropriate context data.
    """
     
    # Initialize variables
    message = None
    deposit_form = AddMoneyForm()
    withdraw_form = WithdrawMoneyForm()

    # Check if the form has been submitted if it has get its action
    if request.method == 'POST':
        action = request.POST.get('action')

        # If the action is to deposit money: 
        if action == 'deposit':

            # Create an instance of the AddMoneyForm with the submitted data
            deposit_form = AddMoneyForm(request.POST)

            # If the form is valid
            if deposit_form.is_valid():

                #Try to find the account with the given account number
                try:
                    account = InmateFinancialAccount.objects.get(account_number=deposit_form.cleaned_data['account_number'])
                except InmateFinancialAccount.DoesNotExist:
                    account = None

                # If the account exists
                if account:

                    #Update the account balance and create a new transactino
                    account.balance = account.balance + deposit_form.cleaned_data['amount']
                    transaction = TransactionDetail.objects.create(
                        account_number=account, transaction_type='D',
                        transaction_amount=deposit_form.cleaned_data['amount'],
                        transaction_date=timezone.now(),
                        transaction_performed_by=request.user,
                    )

                    # Save the changes to the account and the transaction
                    account.save()
                    transaction.save()

                    # Set a success message to display to the user
                    message = 'Money added successfully'

                else:

                    # Set an error message to display to the user
                    message = 'Account does not exist'

        # If the action is to withdraw money
        elif action == 'withdraw':

            # Create an instance of the WithdrawMoneyForm with the submitted data
            withdraw_form = WithdrawMoneyForm(request.POST)

            #If the form is valid
            if withdraw_form.is_valid():

                # Try to find the account with the given account number
                try:
                    account = InmateFinancialAccount.objects.get(account_number=withdraw_form.cleaned_data['account_number'])
                
                # If the account does not exist set it equal to none
                except InmateFinancialAccount.DoesNotExist:
                    account = None

                # If the account exists update its balance
                if account:

                    # If the balance goes below zero set an error message that there are not enough funds
                    if account.balance - withdraw_form.cleaned_data['amount'] < 0:
                        message = 'Insufficient funds'

                    #Update the account balance and create a new transactino
                    else:
                        account.balance = account.balance - withdraw_form.cleaned_data['amount']
                        transaction = TransactionDetail.objects.create(
                            account_number=account, transaction_type='W',
                            transaction_amount=withdraw_form.cleaned_data['amount'],
                            transaction_date=timezone.now(),
                            transaction_performed_by=request.user,
                        )

                        # Save the changes to the account and the transaction
                        account.save()
                        transaction.save()

                        # Set an success message that there withdraw is successful
                        message = 'Money withdrawn successfully'

                # If the account does not exist set an error messege that the account does not exist
                else:
                    message = 'Account does not exist'

    # Get the transaction history for the current user
    transactions = TransactionDetail.objects.filter(transaction_performed_by=request.user)

    # Create a dictionary of variables to pass to the template
    context = {
        'user_position': request.user.position,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'message': message,
    }

    # Render the accounts_home template with the updated context data.
    return render(request, 'financial/accounts_home.html', context)

@login_required
def accounts_transaction_details(request):
    accounts = InmateFinancialAccount.objects.all()
    context = {'accounts': accounts}
    return render(request, 'financial/accounts_search_number.html', context)

@login_required
def accounts_search_name(request):
    return render(request, 'financial/accounts_search_name.html')

@login_required
def get_all_accounts(request):
    accounts = InmateFinancialAccount.objects.all()
    context = {'accounts': accounts}
    return render(request, 'financial/account_list.html', context)

@login_required
def get_all_transaction_details(request):
    if request.method == 'POST':
        filter_by = request.POST.get('search_num')
        if filter_by:
            transaction_details = TransactionDetail.objects.filter(account_number=filter_by)
            context = {'transaction_details': transaction_details}
            return render(request, 'financial/transaction_details_list.html', context)

    return render(request, 'financial/transaction_details_list.html')

def add_money(request):  
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            try:
             account = InmateFinancialAccount.objects.get(account_number=form.cleaned_data['account_number'])
            except InmateFinancialAccount.DoesNotExist:
                account = None

            if(account):
                account.balance = account.balance + form.cleaned_data['amount']
                transaction = TransactionDetail.objects.create(
                account_number=account, transaction_type='D', 
                transaction_amount=form.cleaned_data['amount'], 
                transaction_date=timezone.now(),
                transaction_performed_by=request.user,  
                )
                
                transaction = TransactionDetail.objects.create(
                account_number=account, transaction_type='D', 
                transaction_amount=form.cleaned_data['amount'], 
                transaction_date=timezone.now(),
                transaction_performed_by=request.user,  
                )
                
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
             account = InmateFinancialAccount.objects.get(account_number=form.cleaned_data['account_number'])
            except InmateFinancialAccount.DoesNotExist:
                account = None

            if(account):
                money = form.cleaned_data['amount']
                if (account.balance-money < 0):
                    return render(request, 'withdraw_money.html', {'message': 'Insufficient funds'})
                else:
                    account.balance = account.balance - money
                    print(type(money))
                    transaction = TransactionDetail.objects.create(
                        account_number=account, transaction_type='W', 
                        transaction_amount=form.cleaned_data['amount'], 
                        transaction_date=timezone.now(),
                        transaction_performed_by=request.user,
                    )
                    account.save()
                    transaction.save()


                    return render(request, 'withdraw_money.html', {'message': 'Money withdrawn successfully'})
            else:
                return render(request, 'withdraw_money.html', {'message': 'Account does not exist'})
    else:
        form = WithdrawMoneyForm()
    return render(request, 'withdraw_money.html', {'form': form})
    
def view_inmate(request):
    return render(request, 'inmates/view_inmate.html')

def get_inmate_details(request):
    if request.method == 'POST':
        filter_by = request.POST.get('search_type')
        if filter_by == 'full_list':
            inmate_list = InmateTraits.objects.all()
            context = {'inmate_list': inmate_list}
            return render(request, 'inmates/inmate_result.html', context)
        
        if filter_by == 'by_first_name':
            search_var = request.POST.get('search-box')
            try:
                inmate = InmateTraits.objects.filter(first_name=search_var)
            except InmateTraits.DoesNotExist:
                return render(request, 'inmates/view_inmate.html')
            context= {'by_first_name': inmate}
            try: 
                return render(request, 'inmates/inmate_result.html', context)
            except InmateTraits.MultipleObjectsReturned:
                return render(request, 'inmates/view_inmate.html')
    
        if filter_by == 'by_last_name':
            search_var = request.POST.get('search-box')
            try:
                inmate = InmateTraits.objects.filter(last_name=search_var)
            except InmateTraits.DoesNotExist:
                return render(request, 'inmates/view_inmate.html')
            context= {'by_last_name': inmate}
            try: 
                return render(request, 'inmates/inmate_result.html', context)
            except InmateTraits.MultipleObjectsReturned:
                return render(request, 'inmates/view_inmate.html')
    
        if filter_by == 'by_id':
            search_var = request.POST.get('search-box')
            try:
                inmate = InmateTraits.objects.filter(id=search_var)
            except InmateTraits.DoesNotExist:
                None
            context= {'by_id': inmate}
            return render(request, 'inmates/inmate_result.html', context)
                
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
    return render(request, 'booking/add_inmate.html', {'inmate_traits_form': form})

def add_inmate_arrest_information(request):

    if request.method == 'POST':

        form = InmateArrestingInfoForm(request.POST)
        
        if form.is_valid():
            request.session['inmate_arrest_info_data'] = request.POST
            return redirect('inmate_health_sheet')
    else:
        form = InmateArrestingInfoForm(initial=request.session.get('inmate_arrest_info_data', None))

    return render(request, 'booking/inmate_arrest_info.html', {'inmate_arrest_info_form': form})

def add_inmate_health_sheet(request):

    # If the request method is POST process the form data
    if request.method == 'POST':

        # Create a form object with the POST data
        form = InmateHealthSheetForm(request.POST)
        
        # If the form is valid save the POST data to the session and redirect to the next page
        if form.is_valid():
            request.session['inmate_health_sheet_data'] = request.POST
            return redirect('inmate_gang_affiliation')
    # If the request method is GET render a blank form
    else:
        form = InmateHealthSheetForm(initial=request.session.get('inmate_health_sheet_data', None))

    # Render the inmate_health_sheet.html template with the form object as a context variable
    return render(request, 'booking/inmate_health_sheet.html', {'inmate_health_sheet_form': form})


def add_inmate_gang_affiliation(request):

    if request.method == 'POST':

        form = InmateGangAffiliationForm(request.POST)
        
        if form.is_valid():
            request.session['inmate_gang_affiliation_data'] = request.POST
            return redirect('inmate_vehicle_disposition')
        
    else:
        form = InmateGangAffiliationForm(initial=request.session.get('inmate_gang_affiliation_data', None))

    return render(request, 'booking/inmate_gang_affiliation.html', {'inmate_gang_affiliation_form': form})

def add_inmate_vehicle_disposition(request):

    # If the request method is POST process the form data
    if request.method == 'POST':

        # Create a form object with the POST data
        form = InmateVehicleDispositionForm(request.POST)
        
        # If the form is valid save the POST data to the session and redirect to the next page
        if form.is_valid():
            request.session['inmate_vehicle_disposition_data'] = request.POST
            return redirect('inmate_property')
        
    # If the request method is GET, render a blank form
    else:
        form = InmateVehicleDispositionForm(initial=request.session.get('inmate_vehicle_disposition_data', None))

    # Render the inmate_arrest_info.html template with the form object as a context variable
    return render(request, 'booking/inmate_vehicle_disposition.html', {'inmate_vehicle_disposition_form': form})


def add_inmate_property(request):
    if request.method == 'POST':
        form = InmatePropertyForm(request.POST)

        if form.is_valid():
            inmate_form = InmateForm(request.session['inmate_traits_data'])
            arrest_info_form = InmateArrestingInfoForm(request.session['inmate_arrest_info_data'])
            health_sheet_form = InmateHealthSheetForm(request.session['inmate_health_sheet_data'])
            gang_affiliation_form = InmateGangAffiliationForm(request.session['inmate_gang_affiliation_data'])
            vehicle_disposition_form = InmateVehicleDispositionForm(request.session['inmate_vehicle_disposition_data'])

            if (inmate_form.is_valid() and arrest_info_form.is_valid() and
                    health_sheet_form.is_valid() and gang_affiliation_form.is_valid() and
                    vehicle_disposition_form.is_valid()):

                traits = inmate_form.save()
                arrest_info = arrest_info_form.save()
                health_sheet = health_sheet_form.save()
                gang_affiliation = gang_affiliation_form.save()
                vehicle_disposition = vehicle_disposition_form.save()
                inmate_property = form.save()

                # Retrieve the last account created in the Account model
                last_account = InmateFinancialAccount.objects.last()
                
                # If a last account exists increment its account_number by 1 to generate the next account number
                # If no accounts exist (i.e., the database is empty) set the account_number to 1 for the first account
                next_account_number = (last_account.account_number + 1) if last_account else 1

                # Create an Account instance and save it
                inmate_account = InmateFinancialAccount.objects.create(
                    account_number=next_account_number,
                    balance=0.0
                )

                inmate_account.save()

                # Create and save the InmateInformationSheet instance
                inmate_sheet = InmateInformationSheet.objects.create(
                    traits=traits,
                    arrest_info=arrest_info,
                    health_sheet=health_sheet,
                    gang_name=gang_affiliation,
                    license_plate_number=vehicle_disposition,
                    property=inmate_property,
                    account_number = inmate_account
                )

                inmate_sheet.save()

                return render(request, 'booking/inmate_confirmation.html')

    else:
        form = InmatePropertyForm(initial=request.session.get('inmate_property_data', None))

    return render(request, 'booking/inmate_property.html', {'inmate_property_form': form})


def create_user_success(request):
    return render(request, 'create_user_success.html')

def inventory(request):
    inventory_list = InmateProperty.objects.all()
    context = {'inventory_list': inventory_list}
    return render(request, 'inventory/inventory.html', context)

def update_release_status(request):
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        release_status = request.POST.get('release_status')
        try:
            # Retrieve the InmateProperty object to be updated
            inmate_property = InmateProperty.objects.get(id=property_id)
            # Update the release_status field
            inmate_property.release_status = release_status
            # Save the updated object
            inmate_property.save()
            # Redirect to a success page
            return redirect('success_page')
        except InmateProperty.DoesNotExist:
            # Handle case where InmateProperty object does not exist
            # Redirect to an error page
            return redirect('fail_page')
    else:
        # Handle case where request method is not POST
        # Redirect to an error page
        return redirect('fail_page')

def update_release_status_success(request):
    return render(request, 'inventory/update_release_status_success.html')

def update_release_status_fail(request):
    return render(request, 'inventory/update_release_status_fail.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout_success'))

def logout_success(request):
    return render(request, 'user/logout_success.html')
