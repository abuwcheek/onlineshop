from django import forms
from django.forms.widgets import TextInput, PasswordInput, EmailInput
from .models import User, UserResetPassword
from apps.base.utilits import VerifyEmailCode, CODE_LENGTH

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'first name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'last name'}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'email'}), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'phone'}), required=True)

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm_password'}), required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email oldin ro'yxatdan o'tgan")

        return email


    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Parollar bir biriga mos emas!")

        return password2


    def save(self, commit=True):
        password = self.cleaned_data.get('password')

        user = super().save(commit)
        user.set_password(password)
        user.save()

        return user



class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email'}), required=True)
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not email or not password:
            raise forms.ValidationError("Maydonlar bo'sh bo'lmasligi lozim")

        return self.cleaned_data



class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('first_name', 'last_name', 'email', 'phone', 'photo')



class PasswordResetForm(forms.ModelForm):
    email = forms.EmailField( widget=TextInput(attrs={'placeholder': 'email address'}), required=True)


    class Meta:
        model=UserResetPassword
        fields=('email',)

    def clean(self):
        email = self.cleaned_data.get('email')
        is_email = User.objects.filter(email=email).exists()
        if not is_email:
            raise forms.ValidationError("Bunday emailga ega foydalanuvchi topilmadi!")

        return self.cleaned_data


    def save(self, commit=True):
        code_obj = VerifyEmailCode()
        code = code_obj.new_code()

        verify = super().save()
        verify.code = code
        verify.save()

        return verify


class CheckVerifyCodeForm(forms.Form):
    code = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Kodni kiriting...'}), required=True)

    def clean(self):
        code = self.cleaned_data.get('code')

        if not code or not code.isnumeric() or len(code) != CODE_LENGTH:
            raise forms.ValidationError("Kod noto'g'ri formatda kiritildi!!!")

        return self.cleaned_data



class PasswordResetConfirmForm(forms.Form):
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}), required=False)

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Parollar bir-biriga mos emas!")

        return password2
