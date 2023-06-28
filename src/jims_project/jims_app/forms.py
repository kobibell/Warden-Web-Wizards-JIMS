from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class DepositMoneyForm(forms.Form):
    """
    Form for depositing money to an account.
    """
    account_number = forms.CharField(max_length=200)
    amount = forms.FloatField()

class WithdrawMoneyForm(forms.Form):
    """
    Form for withdrawing money from an account.
    """
    account_number = forms.CharField(max_length=200)
    amount = forms.FloatField()


#! NOTE : NOT NEEDED (TESTSING)
# class SignUpForm(UserCreationForm):
#     """
#     Form for user registration (sign up).
#     Extends the UserCreationForm provided by Django.
#     """
#     first_name = forms.CharField(max_length=30, required=False)
#     last_name = forms.CharField(max_length=30, required=False)
#     email = forms.EmailField(max_length=254, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )

class InmateForm(forms.ModelForm):
    """
    Form for creating or updating inmate traits.
    """

    class Meta:
        model = InmateTraits
        fields = '__all__'
        widgets = {
            'middle_initial': forms.TextInput(attrs={'size': '1', 'maxlength': '1'}),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'sex': forms.Select,
            'height_feet': forms.Select,
            'height_inches': forms.Select,
            'country' : forms.Select,
            'nationality' : forms.Select,
        }
        labels = {
            'primary_add': 'Primary Address',
            'temp_add': 'Temporary Address',
        }

class InmateHealthSheetForm(forms.ModelForm):
    """
    Form for creating or updating inmate health sheets.
    """

    class Meta:
        model = InmateHealthSheet
        fields = '__all__'

class InmateArrestingInfoForm(forms.ModelForm):
    """
    Form for creating or updating inmate arresting information.
    """

    class Meta:
        model = InmateArrestInfo
        fields = '__all__'
        widgets = {
            'arrest_timestamp': forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }

class InmatePropertyForm(forms.ModelForm):
    """
    Form for creating or updating inmate properties.
    """

    class Meta:
        model = InmateProperty
        fields = '__all__'

class InmateVehicleDispositionForm(forms.ModelForm):
    """
    Form for creating or updating inmate vehicle dispositions.
    """

    class Meta:
        model = InmateVehicles
        fields = '__all__'
        
class InmateGangAffiliationForm(forms.ModelForm):
    """
    Form for creating or updating inmate gang affiliations.
    """
    
    class Meta:
        model = InmateGangs
        fields = '__all__'
