from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Accounts
from .models import TransactionDetails

from .forms import AddMoneyForm
from .forms import WithdrawMoneyForm

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

def accounts_transaction_details(request):
    return render(request, 'accounts_search_number.html')  

def accounts_search_name(request):
    return render(request, 'accounts_search_name.html')

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
                transaction = TransactionDetails.objects.create(account_number_id=account.account_number, transaction_type='D', transaction_amount=form.cleaned_data['amount'], transaction_date=timezone.now())
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
    