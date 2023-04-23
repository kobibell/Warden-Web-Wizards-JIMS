from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import InmateTraits

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
    

