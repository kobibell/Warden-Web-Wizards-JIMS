from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django import forms
from django_countries.fields import CountryField
from localflavor.us.models import USStateField
# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    A custom manager for the CustomUser model that extends Django's BaseUserManager.

    This manager provides methods for creating and managing custom users 

    Args:
        BaseUserManager (Class) : Django's BaseUserManager Class
    """
    def create_user(self, email, user_name, first_name, last_name, password, position, **other_fields):
        """
        Creates a new custom user instance with the given fields.

        Args:
            email (str): The email address of the user
            user_name (str): The username of the user
            first_name (str): the first name of the user
            last_name (str): the last name of the user
            password (str): the password of the user
            position (str): the position of the user

        Returns:
            CustomUser: A newly created user instance
        """
        
        # Normalzie the email to contain only lowercase values
        email = self.normalize_email(email)

        #Create an instance a user using Djanos underlying base user manager
        user = self.model(email=email, user_name=user_name, first_name = first_name, last_name = last_name, position = position, **other_fields)

        #For the current user instance take has the users password
        user.set_password(password)

        #Save the user
        user.save(using=self._db) 

        #Print for testing
        print(f"User created: username={user_name}, password={password}, password_hash={user.password}")
        
        return user

    def create_superuser(self, email, password, first_name, last_name, **other_fields):
        """
        Creates a new superuser instance with the given fields.

        Args:
            email (str): The email address of the user
            password (str): The password of the user
            first_name (str): The first name of the user
            last_name (str): The last name of the user
            **other_fields: Additional fields to be set on the user

        Returns:
            CustomUser: A newly created superuser instance
        """

        # A super user will have an additional field is_staff which by default should be true
        # Note : This staff is assocaited with staff of the Djano Admin not the JIMS System
        other_fields.setdefault('is_staff', True)

        # A super user will have an additional field is_superuser which by default should be true
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, password=password, first_name=first_name, last_name=last_name, **other_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model that extends Django's built-in AbstractBaseUser and PermissionsMixin.

    The purpose of this class is to define a custom user model that we can use to create user accounts with custom fields and functions beyond the defualy fields provided by Django
    """

    # A custom user will be one of four positions
    POSITION_CHOICES = (
        ('officer', 'officer'),
        ('booking_clerk', 'booking_clerk'),
        ('supervisor', 'supervisor'),
        ('release_clerk', 'release_clerk'),
    )

    #The feilds of a Custom User
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=25, choices=POSITION_CHOICES)
    user_status = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Define the username field that user will login with is their email
    USERNAME_FIELD = 'email'

    # In order to create a custom user a user name, first name last name and a position are required
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name', 'position']

    objects = CustomUserManager()

class Officer(models.Model):
    """
    Create an Supervisor model 
    
    A Officer model IS-A Custom User that HAS-A officer_id
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    officer_id = models.CharField(max_length=200, null=False)

class BookingClerk(models.Model):
    """
    Create an Supervisor model which IS-A Custom User that HAS-A booking_clerk_id
    """

    #The feilds of a Booking Clerk
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    booking_clerk_id = models.CharField(max_length=200, null=False)


class Supervisor(models.Model):
    """
    Create an Supervisor model which IS-A Custom User that HAS-A supervisor ID
    """

    #The feilds of a Supervisor
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    supervisor_id = models.CharField(max_length=200, null=False)


class ReleaseClerk(models.Model):
    """
    Create an Release Clerk model which IS-A Custom User that HAS-A release_clerk_id
    """

    #The feilds of a ReleaseClerk
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    release_clerk_id = models.CharField(max_length=200, null=False)


class Accounts(models.Model):
    """
    Create an Accounts model (database) HAS-A account_number, account_type, and balance
    """

    # The fields of Accounts
    account_number = models.IntegerField(null=False, primary_key=True)
    balance = models.FloatField(null=False)

class TransactionDetails(models.Model):
    """
    Create a TransactionDetails model (database) with the transaction_id, transaction_type, transaction_amount, and transaction_date
    """
    transaction_id = models.AutoField(primary_key=True)
    account_number = models.ForeignKey(Accounts, null=False, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=2, null=False)
    transaction_amount = models.FloatField(null=False)
    transaction_date = models.DateTimeField(null=False)
    transaction_performed_by = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)

class InmateTraits(models.Model):
    
    """
    Create an InmateTraits Model (database) with the details below
    """
    SEX_CHOICES = [
        ('W', 'Woman'),
        ('M', 'Man'),
        ('T', 'Transgender'),
        ('N', 'Non-binary/non-conforming'),
        ('P', 'Prefer not to respond'),
    ]

    HAIR_COLOR_CHOICES = (
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('blonde', 'Blonde'),
        ('red', 'Red'),
        ('gray', 'Gray'),
        ('white', 'White'),
        ('other', 'Other'),
    )

    EYE_COLOR_CHOICES = (
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('gray', 'Gray'),
        ('hazel', 'Hazel'),
        ('other', 'Other'),
    )

    FEET_CHOICES = [(i, f'{i} ft') for i in range(2, 8)]
    INCHES_CHOICES = [(i, f'{i} in') for i in range(0, 12)]

    first_name = models.CharField(max_length=80)
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    last_name = models.CharField(max_length=80)
    date_of_birth = models.DateField()
    place_of_birth = CountryField()
    # nationality = models.CharField(max_length=80)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    hair_color = models.CharField(max_length=20, choices=HAIR_COLOR_CHOICES)
    eye_color = models.CharField(max_length=20, choices=EYE_COLOR_CHOICES)
    height_feet = models.PositiveIntegerField(choices=FEET_CHOICES)
    height_inches = models.PositiveIntegerField(choices=INCHES_CHOICES)
    weight = models.PositiveIntegerField()
    alias = models.CharField(max_length=80, blank=True, null=True)
    blemishes = models.CharField(max_length=200, blank=True, null=True)
    primary_address = models.CharField(max_length=200)
    secondary_adress = models.CharField(max_length=200, blank=True, null=True)
    drivers_license_num = models.CharField(max_length=8, unique=True)
    drivers_license_state = USStateField()
    date_added = models.DateTimeField(null=False, default=timezone.now)

class InmateArrestInfo(models.Model):
    arrest_timestamp = models.DateTimeField()
    arresting_agency = models.CharField(max_length=100)
    arresting_location = models.CharField(max_length=100)
    arresting_charges = models.CharField(max_length=225)
    arresting_officer_id = models.IntegerField()
    searching_officer_id = models.IntegerField()
    transporting_officer_id = models.IntegerField()
    dept_report_number = models.IntegerField()
    bail_allowance = models.BooleanField()
    bail_amount = models.DecimalField(max_digits=8, decimal_places=2)

class InmateVehicles(models.Model):
    license_plate_number = models.CharField(max_length=7, primary_key=True)
    license_plate_state = models.CharField(max_length=2)
    make = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    place_parked = models.CharField(max_length=100)
    impound_company = models.CharField(max_length=100)
    impound_location = models.CharField(max_length=100)

class InmateHealthSheet(models.Model):
    epilepsy = models.CharField(max_length=225)
    escape_risk = models.BooleanField()
    head_lice = models.CharField(max_length=225)
    body_lice = models.CharField(max_length=225)
    heart_disease = models.CharField(max_length=225)
    impaired_consciousness = models.CharField(max_length=100)
    medications = models.CharField(max_length=225)
    mental_disorder = models.CharField(max_length=225)
    emergency_care = models.CharField(max_length=225)
    suicide_risk = models.CharField(max_length=225)
    uses_drugs = models.CharField(max_length=225)
    uses_alcohol = models.CharField(max_length=225)

class InmateProperty(models.Model):
    type_of_property = models.CharField(max_length=100)
    description = models.CharField(max_length=225)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=50)
    release_status = models.BooleanField()

class EmergencyContacts(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=10)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

class InmateGangs(models.Model):
    gang_name = models.CharField(max_length=50, primary_key=True)
    gang_area = models.CharField(max_length=50)
    is_active = models.BooleanField()

class InmateSheet(models.Model):
    traits = models.OneToOneField(InmateTraits, on_delete=models.CASCADE)
    arrest_info = models.OneToOneField(InmateArrestInfo, on_delete=models.CASCADE)
    health_sheet = models.OneToOneField(InmateHealthSheet, on_delete=models.CASCADE)
    license_plate_number = models.OneToOneField(InmateVehicles, on_delete=models.SET_NULL, null=True)
    property = models.OneToOneField(InmateProperty, on_delete=models.SET_NULL, null=True)
    gang_name = models.OneToOneField(InmateGangs, on_delete=models.SET_NULL, null=True)
    emergency_contact = models.OneToOneField(EmergencyContacts, on_delete=models.SET_NULL, null=True)
    account_number = models.OneToOneField(Accounts, on_delete=models.CASCADE, default=None)
