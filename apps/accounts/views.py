from datetime import datetime
from apps.base.utilits import send_mail_code
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterUserForm, LoginForm, UpdateUserForm, PasswordResetForm, CheckVerifyCodeForm, PasswordResetConfirmForm
from django.views import View
from django.contrib import messages
from .models import User, UserResetPassword
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView

class RegisterUserView(View):
    form_class = RegisterUserForm

    def get(self, request):
        form=self.form_class()
        context={
            'form': form,
        }

        return render(request, 'accounts/register.html', context)

    def post(self, request):
        user_form=self.form_class(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.info(request, "Ro'yxatdan o'tdingiz!")
            return redirect('home')

        messages.warning(request, "Ro'yxatdan o'ta olmadingiz!!!")
        context = {
            'form': user_form,
        }
        return render(request, 'accounts/register.html', context)



class LoginUserView(View):
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        contex = {
            'form': form,
        }

        return render(request, 'accounts/login.html', contex)

    def post(self, request):
        user_form = self.form_class(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, "Tizimga muvaffaqiyatli kirdingiz.")
                return redirect('index')

            messages.errors(request, "Login yoki parol noto'g'ri.")
            contex = {
                'form': user_form,
            }

            return render(request, 'accounts/login.html', contex)

        messages.error(request, user_form.errors)
        contex = {
            'form': user_form,
        }

        return render(request, 'accounts/login.html', contex)


class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.info(request, "Tizimdan muvaffaqiyatli chiqtingiz. ")
        return redirect('home')



class UpdateUserView(View):
    form_class = UpdateUserForm
    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request,'accounts/update-profile.html', {'form': form})


    def post(self, request):
        user_form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()

            messages.success(request, "Profil muvaffaqiyatli yangilandi.")
            return redirect("home")

        messages.warning(request, "Profil yangilanmadi!!!")
        return render(request,'accounts/update-profile.html', {'form': user_form})


class PasswordResetView(View):
    form_class = PasswordResetForm

    def get(self, request):
        form = self.form_class()
        context = {
            'form': form,
        }
        return render(request, 'accounts/password_reset_form.html', context)

    def post(self, request, *args, **kwargs):
        email_form = self.form_class(request.POST)
        if email_form.is_valid():
            verify = email_form.save()
            send_mail_code(verify.email, verify.code)

            messages.info(request, "Emailingizga kod yuborildi.")
            return redirect('accounts:check-code', uuid=verify.id)

        messages.error(request, email_form.errors)
        return render(request, 'accounts/password_reset_form.html', {'form': email_form})


class CheckVerifyCodeView(View):
    form_class = CheckVerifyCodeForm

    def get(self, request, uuid):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, 'accounts/password_reset_check_verify_code.html', context)


    def post(self, request, uuid):
        verify_form = self.form_class(request.POST)
        if not verify_form.is_valid():
            messages.error(request, verify_form.errors)
            return render(request, 'accounts/password_reset_check_verify_code.html', {'form': verify_form})

        code = verify_form.cleaned_data.get('code')

        verify_code = UserResetPassword.objects.filter(id=uuid, expiration_time__gte=datetime.now(), is_confirmation=False, code=code).first()
        if not verify_code:
            messages.warning(request, "Kod xato yoki vaqti tugagan. ")
            return render(request, 'accounts/password_reset_check_verify_code.html', {'form': verify_form})

        verify_code.is_confirmation = True
        verify_code.save()

        messages.info(request, "Kod to'g'ri, endi yangi parol kiriting.")
        return redirect('accounts:password-reset-confirm', uuid=uuid)



class PasswordResetConfirmView(View):
    form_class = PasswordResetConfirmForm

    def get(self, request, uuid):
        form = self.form_class()
        contex = {
            'form': form
        }

        return render(request, 'accounts/password_reset_confirm.html', contex)

    def post(self, request, uuid):
        password_form = self.form_class(request.POST)
        if password_form.is_valid():
            email = UserResetPassword.objects.get(id=uuid).email
            user = User.objects.get(email=email)
            password = password_form.cleaned_data.get("password")

            user.set_password(password)
            user.save()

            messages.success(request, "Parolingiz o'zgartirildi.")
            return redirect('accounts:login')

        messages.warning(request, "Parollar bir-biriga mos emas.")
        return render(request, 'accounts/password_reset_confirm.html', {'form': password_form})



# class MyProfileView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             user = User.objects.get(id = request.user)
#             context = {
#                 'user': user,
#             }
#             return render(request, 'accounts/profile.html', context)
#         messages.warning(request, 'Siz oldin Login qilishingiz kerak.')
#         return redirect('accounts:login')