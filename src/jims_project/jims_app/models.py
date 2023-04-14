from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Person(models.Model):
    """
    Create a Person model (database) with the first_name, last_name
    """

    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)

class Officer(models.Model):
    """
    Create an Officer model (database) with officer_id, last_name, and user_password
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    officer_id = models.CharField(max_length=200, null=False)
    user_password = models.CharField(max_length=200, null=False)

class Accounts(models.Model):
    """
    Create an Accounts model (database) with the account_number, account_type, and balance
    """
    account_number = models.CharField(max_length=200, null=False, primary_key=True)
    inmate_id = models.CharField(max_length=200, null=False)
    balance = models.FloatField(null=False)

class TransactionDetails(models.Model):
    """
    Create a TransactionDetails model (database) with the transaction_id, transaction_type, transaction_amount, and transaction_date
    """
    transaction_id = models.CharField(max_length=200, null=False, primary_key=True, auto_created=True)
    account_number = models.CharField(max_length=200, null=False)
    transaction_type = models.CharField(max_length=2, null=False)
    transaction_amount = models.FloatField(null=False)
    transaction_date = models.DateTimeField(null=False)