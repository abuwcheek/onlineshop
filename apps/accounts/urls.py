from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutView,
    UpdateUserView,
    PasswordResetView,
    CheckVerifyCodeView,
    PasswordResetConfirmView,
    MyProfileView,
)

from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('register-user/', RegisterUserView.as_view(), name='register'),
    path('login-user/', LoginUserView.as_view(), name='login'),
    path('logout-user/', LogoutView.as_view(), name='logout'),
    path('user-profile/', MyProfileView.as_view(), name='profile'),
    path('update-profile/', UpdateUserView.as_view(), name='update'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path( 'check-verify-code/<uuid:uuid>/', CheckVerifyCodeView.as_view(), name='check-code'),
    path('password-reset-confirm/<uuid:uuid>', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]