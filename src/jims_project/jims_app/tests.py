from getpass import getuser
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
from urllib.parse import urlencode


import json

from jims_app.models import *
from jims_app.forms import AddMoneyForm

# Create your tests here.
class HomePageTest(TestCase):

    def setUp(self):
        '''
        Set up user for test executions
        '''
        self.user = CustomUser.objects.create_user(email="chunckycop@police.com", user_name="chunckycop@police.com", first_name="chunky", last_name="cop",
        password="glazed", position="supervisor")
        self.user.save()

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
        credential=dict()
        credential["username"]="chunkycop@police.com"
        credential["password"]="glazed"
        response = self.client.post('/login/', data=json.dumps(credential), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        '''
        Test logout redirects to base page
        '''
        response = self.client.get('/logout/')
        self.assertRedirects(response,"/")

class UserPageTest(TestCase):
    
    def setUp(self):
        '''
        Set up user, accounts and Transactions details for testing
        '''
        self.user = CustomUser.objects.create(user_name="chunkycop@police.com", password="glazed", first_name="Chuck", last_name="Cop", position="supervisor")
        self.user.save()
        credential=dict()
        credential["username"]="chunkycop@police.com"
        credential["password"]="glazed"
        response = self.client.post('/login/', data=json.dumps(credential), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        Accounts.objects.create(account_number="0001", inmate_id = "0001", balance=0)
        TransactionDetails.objects.create(account_number=Accounts.objects.filter(account_number="0001")[0], transaction_type="D", transaction_amount=0, transaction_date="2020-10-10")
        
    def tearDown(self):
        '''
        Tear down all setup
        '''
        self.user.delete()
        Accounts.objects.all().delete()

    def test_url_exists_at_correct_location(self):
        '''
        Test add money url exists at correct location
        '''
        response = self.client.get("/accounts/add_money/")
        self.assertEqual(response.status_code, 200)
    
    def test_add_money_form(self):
        '''
        Test valid form is created from data for processing
        '''
        data = dict({"account_number": "0001", "amount": 100})
        data = AddMoneyForm(data)
        self.assertTrue(data.is_valid())

    def test_add_money(self):
        '''
        Test add money to account
        '''
        data = urlencode({'account_number': '0001', 'amount': '100'})
        response = self.client.post("/accounts/add_money/", data, content_type='application/x-www-form-urlencoded', follow=True)
        self.assertEqual(response.status_code, 200)
        accounts = Accounts.objects.filter(account_number="0001")
        self.assertEqual(accounts[0].balance, 100)

    def test_withdraw_money(self):
        '''
        Test withdraw money from account
        '''
        data = urlencode({'account_number': '0001', 'amount': '100'})
        response = self.client.post("/accounts/withdraw_money/", data, content_type='application/x-www-form-urlencoded', follow=True)
        self.assertEqual(response.status_code, 200)
        accounts = Accounts.objects.filter(account_number="0001")
        self.assertEqual(accounts[0].balance, 0)

    def test_get_all_transactions(self):
        '''
        Test transaction details get updated with add money function
        '''
        data = urlencode({'account_number': '0001', 'amount': '100'})
        response = self.client.post("/accounts/add_money/", data, content_type='application/x-www-form-urlencoded', follow=True)
        self.assertEqual(response.status_code, 200)

        data = urlencode({'search_num': '0001'})
        response = self.client.post("/accounts/transactions-details/", data, content_type='application/x-www-form-urlencoded', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TransactionDetails.objects.all().count(), 2)
