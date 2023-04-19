from django import forms


class AddMoneyForm(forms.Form):
    account_number = forms.CharField(max_length=200)
    amount = forms.FloatField()

class WithdrawMoneyForm(forms.Form):
    account_number = forms.CharField(max_length=200)
    amount = forms.FloatField()
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AddInmate


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )

class InmateForm(forms.ModelForm):
    class Meta:
        model = AddInmate
        fields = '__all__'
        widgets = {
            'middle_initial': forms.TextInput(attrs={'size': '1', 'maxlength': '1'}),
        }
