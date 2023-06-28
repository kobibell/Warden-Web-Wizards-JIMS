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
    """
    def create_user(self, email, user_name, first_name, last_name, password, position, **other_fields):
        """
        Creates a new custom user instance with the given fields.

        Args:
            email (str): The email address of the user.
            user_name (str): The username of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            password (str): The password of the user.
            position (str): The position of the user.
            **other_fields: Additional fields to be set on the user.

        Returns:
            CustomUser: A newly created user instance.
        """
        
        # Normalize the email to contain only lowercase values
        email = self.normalize_email(email)

        # Create an instance of a user using Django's underlying base user manager
        user = self.model(email=email, user_name=user_name, first_name = first_name, last_name = last_name, position = position, **other_fields)

        # Set the user's password
        user.set_password(password)

        # Save the user
        user.save(using=self._db) 

        # Print for testing
        print(f"User created: username={user_name}, password={password}, password_hash={user.password}")
        
        return user

    def create_superuser(self, email, password, first_name, last_name, **other_fields):
        """
        Creates a new superuser instance with the given fields.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            **other_fields: Additional fields to be set on the user.

        Returns:
            CustomUser: A newly created superuser instance.
        """

        # A superuser will have the additional field 'is_staff' set to True by default
        # Note: 'is_staff' is associated with staff of the Django Admin, not the JIMS System
        other_fields.setdefault('is_staff', True)

        # A superuser will have the additional field 'is_superuser' set to True by default
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, password=password, first_name=first_name, last_name=last_name, **other_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model that extends Django's AbstractBaseUser and PermissionsMixin.

    This model allows creating user accounts with custom fields and functions beyond the default fields provided by Django.
    """
    
    # The choices avalible for a Custom Users Position
    POSITION_CHOICES = (
        ('Cashier', 'Cashier'),
        ('Booking Clerk', 'Booking Clerk'),
        ('Supervisor', 'Supervisor'),
        ('Release Clerk', 'Release Clerk'),
    )

    #The feilds of a CustomUser
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=25, choices=POSITION_CHOICES)
    user_status = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # The field to use as the unique identifier for the user when logging in
    USERNAME_FIELD = 'email'

    # The fields that are required when creating a user, apart from the username and password
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name', 'position']

    # The manager class to use for creating and managing user instances.
    objects = CustomUserManager()

class Officer(models.Model):
    """
    A model representing an Officer within the JIMS system.

    A Officer IS-A CustomUser
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    officer_id = models.CharField(max_length=200, null=False)

class BookingClerk(models.Model):
    """
    A model representing a Booking Clerk within the JIMS system.

    A Booking Clerk IS-A CustomUser
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    booking_clerk_id = models.CharField(max_length=200, null=False)

class Supervisor(models.Model):
    """
    A model representing a Supervisor within the JIMS system.

    A Supervisor IS-A CustomUser
    """

    #The feilds of a Supervisor
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    supervisor_id = models.CharField(max_length=200, null=False)


class ReleaseClerk(models.Model):
    """
    A model representing a Release Clerk within the JIMS system. 

    A Release Clerk IS-A CustomUser
    """

    #The feilds of a ReleaseClerk
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    release_clerk_id = models.CharField(max_length=200, null=False)


class InmateFinancialAccount(models.Model):
    """
    A model representing an inmate's financial account.
    """

    # The fields of InmateFinancialAccount
    account_number = models.IntegerField(null=False, primary_key=True)
    balance = models.FloatField(null=False)

class TransactionDetail(models.Model):
    """
    A model representing a transaction detail.
    """

    # The fields of a TransactionDetail
    transaction_id = models.AutoField(primary_key=True)
    account_number = models.ForeignKey(InmateFinancialAccount, null=False, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=2, null=False)
    transaction_amount = models.FloatField(null=False)
    transaction_date = models.DateTimeField(null=False)
    transaction_performed_by = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)

class InmateTraits(models.Model):
    """
    A model representing the traits and characteristics of an inmate.
    """

    # The choices avalible for certain feilds
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

    # The fields of a InmateTraits
    profile_picture = models.ImageField(upload_to='inmate_pictures/', blank=True, null=True)
    first_name = models.CharField(max_length=80)
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    last_name = models.CharField(max_length=80)
    date_of_birth = models.DateField()
    place_of_birth = CountryField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    hair_color = models.CharField(max_length=20, choices=HAIR_COLOR_CHOICES)
    eye_color = models.CharField(max_length=20, choices=EYE_COLOR_CHOICES)
    height_feet = models.PositiveIntegerField(choices=FEET_CHOICES)
    height_inches = models.PositiveIntegerField(choices=INCHES_CHOICES)
    weight = models.PositiveIntegerField()
    alias = models.CharField(max_length=80, blank=True, null=True)
    blemishes = models.CharField(max_length=200, blank=True, null=True)
    primary_add = models.CharField(max_length=200)
    temp_add = models.CharField(max_length=200, blank=True, null=True)
    drivers_license_num = models.CharField(max_length=8, unique=True)
    drivers_license_state = USStateField()
    date_added = models.DateTimeField(null=False, default=timezone.now)

class InmateArrestInfo(models.Model):
    """
    A model representing the arrest information of an inmate.
    """

    # The fields of a Inmate Arrest Info
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
    """
    A model representing the vehicles associated with an inmate.
    """

    # The fields of a Inmate Vehicles
    license_plate_number = models.CharField(max_length=7, primary_key=True)
    license_plate_state = models.CharField(max_length=2)
    make = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    place_parked = models.CharField(max_length=100)
    impound_company = models.CharField(max_length=100)
    impound_location = models.CharField(max_length=100)


class InmateHealthSheet(models.Model):
    """
    A model representing the health information of an inmate.
    """

    # The fields of a Inmate Health Sheet
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
    """
    A model representing the property of an inmate.
    """

    # The fields of an Inmates Property
    type_of_property = models.CharField(max_length=100)
    description = models.CharField(max_length=225)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=50)
    release_status = models.BooleanField()


class EmergencyContacts(models.Model):
    """
    A model representing the emergency contacts of an inmate.
    """

    # The fields of an Inmates Emergency Contact
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=10)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)


class InmateGangs(models.Model):
    """
    A model representing the gang affiliations of an inmate.
    """

    # The fields of an Inmates Gang
    gang_name = models.CharField(max_length=50, primary_key=True)
    gang_area = models.CharField(max_length=50)
    is_active = models.BooleanField()


class InmateInformationSheet(models.Model):
    """
    A model that represents an inmate's comprehensive information sheet or information about the inmate.
    """

    # The fields of an Inmates Information Sheet
    traits = models.OneToOneField(InmateTraits, on_delete=models.CASCADE)
    arrest_info = models.OneToOneField(InmateArrestInfo, on_delete=models.CASCADE)
    health_sheet = models.OneToOneField(InmateHealthSheet, on_delete=models.CASCADE)
    license_plate_number = models.OneToOneField(InmateVehicles, on_delete=models.SET_NULL, null=True)
    property = models.OneToOneField(InmateProperty, on_delete=models.SET_NULL, null=True)
    gang_name = models.OneToOneField(InmateGangs, on_delete=models.SET_NULL, null=True)
    emergency_contact = models.OneToOneField(EmergencyContacts, on_delete=models.SET_NULL, null=True)
    account_number = models.OneToOneField(InmateFinancialAccount, on_delete=models.CASCADE, default=None)
