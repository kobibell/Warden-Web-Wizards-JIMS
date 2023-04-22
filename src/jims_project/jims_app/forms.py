from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class AddMoneyForm(forms.Form):
    account_number = forms.CharField(max_length=200)
    amount = forms.FloatField()

class WithdrawMoneyForm(forms.Form):
    account_number = forms.CharField(max_length=200)
    amount = forms.FloatField()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )

class InmateForm(forms.ModelForm):
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

class InmateHealthSheetForm(forms.ModelForm):
    class Meta:
        model = InmateHealthSheet
        fields = '__all__'

class InmateArrestingInfoForm(forms.ModelForm):
    class Meta:
        model = InmateArrestInfo
        fields = '__all__'

class InmatePropertyForm(forms.ModelForm):
    class Meta:
        model = InmateProperty
        fields = '__all__'

class InmateVehicleDispositionForm(forms.ModelForm):
    class Meta:
        model = InmateVehicles
        fields = '__all__'
        
class InmateGangAffiliationForm(forms.ModelForm):
    class Meta:
        model = InmateGangs
        fields = '__all__'

