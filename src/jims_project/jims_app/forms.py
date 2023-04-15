from django import forms


class AddMoneyForm(forms.Form):
    account_number = forms.CharField(max_length=200)
    amount = forms.FloatField()

class WithdrawMoneyForm(forms.Form):
    account_number = forms.CharField(max_length=200)
    amount = forms.FloatField()