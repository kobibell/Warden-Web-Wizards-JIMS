from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
from urllib.parse import urlencode
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model


import json

from jims_app.models import *
from jims_app.forms import AddMoneyForm

# Create your tests here.
class HomePageTest(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create(user_name="chunkycop@police.com", email="chunkycop@police.com", first_name="A", last_name="B", position="supervisor")
        user.set_password("glazed")
        user.save()
    
    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_url_exists_at_correct_location(self):
        '''
        Test if base url exists at correct location
        '''
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_not_access_no_user(self):  
        '''
        Test home page url not accessible without user
        '''
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 302)

    def test_template_name_correct(self):  
        '''
        Test if login page uses correct template
        '''
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "login.html")
    
    def test_login(self):
        '''
        Test login with valid user
        '''
        self.assertFalse(get_user(self.client).is_authenticated)

        credential = urlencode({'username': 'chunkycop@police.com', 'password': 'glazed'})
        response = self.client.post('/', credential, content_type='application/x-www-form-urlencoded')
        self.assertRedirects(response, "/home-page/")

    def test_invalid_login(self):
        '''
        Test login with invalid user
        '''
        self.assertFalse(get_user(self.client).is_authenticated)

        credential = urlencode({'username': 'nouser@police.com', 'password': 'donut'})
        response = self.client.post('/', credential, content_type='application/x-www-form-urlencoded')
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password")

    def test_logout(self):
        '''
        Test logout redirects to base page
        '''
        response = self.client.get('/logout/')
        self.assertRedirects(response,"/logout-success/")

class AccountPagesTest(TestCase):
    
    def setUp(self):
        '''
        Set up user, accounts and Transactions details for testing
        '''
        User = get_user_model()
        user = User.objects.create(user_name="chunkycop@police.com", email="chunkycop@police.com", password="glazed", first_name="A", last_name="B", position="supervisor")
        user.set_password("glazed")
        user.save()

        credential = urlencode({'username': 'chunkycop@police.com', 'password': 'glazed'})
        self.client.post('/', credential, content_type='application/x-www-form-urlencoded')

        Accounts.objects.create(account_number="1", balance=10)
        TransactionDetails.objects.create(account_number=Accounts.objects.filter(account_number="1")[0], transaction_type="D", transaction_amount=0, transaction_date=timezone.now(), transaction_performed_by_id=1)
        
    def tearDown(self):
        '''
        Tear down all setup
        '''
        CustomUser.objects.all().delete()
        Accounts.objects.all().delete()
        TransactionDetails.objects.all().delete()

    def test_url_exists_at_correct_location_add_money(self):
        '''
        Test add money url exists at correct location
        '''
        response = self.client.get(reverse("add_money"))
        self.assertEqual(response.status_code, 200)
    
    def test_url_exists_at_correct_location_withdraw_money(self):
        '''
        Test add money url exists at correct location
        '''
        response = self.client.get(reverse("withdraw_money"))
        self.assertEqual(response.status_code, 200)
    
    def test_add_money_form(self):
        '''
        Test valid form is created from data for processing
        '''
        data = dict({"account_number": "1", "amount": '0'})
        data = AddMoneyForm(data)
        self.assertTrue(data.is_valid())

    def test_add_money(self):
        '''
        Test add money to account
        '''
        data = urlencode({'account_number': '1', 'amount': '100'})
        self.client.post("/accounts/add-money/", data, content_type='application/x-www-form-urlencoded', follow=True)
        
        accounts = Accounts.objects.filter(account_number="1")
        self.assertEqual(accounts[0].balance, 110)
    
    def test_add_money_invalid_account(self):
        '''
        Test add money to account where account number is not valid
        '''
       
        data = urlencode({'account_number': '0002', 'amount': '100'})
        response = self.client.post("/accounts/add-money/", data, content_type='application/x-www-form-urlencoded', follow=True)

        messages = ''.join(list(response.context['message']))
        self.assertEqual(messages, "Account does not exist")
        

    def test_withdraw_money(self):
        '''
        Test withdraw money from account
        '''

        data = urlencode({'account_number': '1', 'amount': '10'})
        response = self.client.post("/accounts/withdraw-money/", data, content_type='application/x-www-form-urlencoded', follow=True)
      
        accounts = Accounts.objects.filter(account_number="1")
        self.assertEqual(accounts[0].balance, 0)

    def test_withdraw_money_invalid_account(self):
        '''
        Test withdraw money to account where account number is not valid
        '''
    
        data = urlencode({'account_number': '0002', 'amount': '100'})
        response = self.client.post("/accounts/withdraw-money/", data, content_type='application/x-www-form-urlencoded', follow=True)
        
        messages = ''.join(list(response.context['message']))
        self.assertEqual(messages, "Account does not exist")
    
    def test_withdraw_money_low_balance(self):
        '''
        Test withdraw money to account where account balance is low
        '''
    
        data = urlencode({'account_number': '1', 'amount': '500'})
        response = self.client.post("/accounts/withdraw-money/", data, content_type='application/x-www-form-urlencoded', follow=True)

        messages = ''.join(list(response.context['message']))
        self.assertEqual(messages, "Insufficient funds")

    def test_get_all_transactions(self):
        '''
        Test transaction details get updated with add money function
        '''

        data = urlencode({'account_number': '1', 'amount': '100'})
        response = self.client.post("/accounts/add-money/", data, content_type='application/x-www-form-urlencoded', follow=True)
        self.assertEqual(response.status_code, 200)

        data = urlencode({'search_num': '1'})
        response = self.client.post("/accounts/transactions-details/", data, content_type='application/x-www-form-urlencoded', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TransactionDetails.objects.all().count(), 2)
    
    def test_get_all_accounts(self):
        '''
        Test get all accounts
        '''
        response = self.client.get("/accounts/account-list/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['accounts'].count(),1)

        """InmateTraits.objects.create(first_name="Chuck", last_name="Smith", date_of_birth="1906-04-22", place_of_birth="US",
                                     sex="M", hair_color="brown", eye_color="brown", height_feet="5", height_inches="6", weight="100",
                                       primary_add="7000 Test Drive", drivers_license_num="B1000000", drivers_license_state="CA", date_added="2023-04-24 18:27:57+00")
        InmateSheet.objects.create(account_number="1", arrest_info=InmateArrestInfo.objects.filter(id="1")[0], emergency_contact=InmateTraits.objects.filter(id="1")[0], gang_name=InmateTraits.objects.filter(id="1")[0], 
                                   health_sheet=InmateTraits.objects.filter(id="1")[0], license_plate_number=InmateTraits.objects.filter(id="1")[0], property="1", traits=InmateTraits.objects.filter(id="1")[0])
        """