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

     def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError("Maydonlar bo'sh bo'lmasligi lozim")
        return country

     
     def clean_address(self):
          address = self.cleaned_data.get('address')
          if not address:
               raise forms.ValidationError("Maydonlar bo'sh bo'lmasligi lozim")
          return address


     def clean_phone(self):
          phone = self.cleaned_data.get('phone')
          if not phone:
               raise forms.ValidationError("Maydonlar bo'sh bo'lmasligi lozim")
          return phone