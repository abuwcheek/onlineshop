from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
     class Meta:
          model = Payment
          fields = ['country', 'address', 'phone']
          widgets = {
               'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'country'}),
               'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'address'}),
               'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'phone'}),
          }