from getpass import getuser
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user

import json

from jims_app.models import CustomUser

# Create your tests here.
class HomePageTest(TestCase):

    def setUpTestData():
        CustomUser.objects.create(user_name="chunkycop@police.com", password="glazed")

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_not_access_no_user(self):  
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 302)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "login.html")
    
    def test_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        credential=dict()
        credential["username"]="chunkycop@police.com"
        credential["password"]="glazed"
        response = self.client.post('/login/', data=json.dumps(credential), content_type='application/json')
        self.assertEqual(response.status_code, 200)