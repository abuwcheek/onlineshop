from django.contrib import admin
from .models import User, UserResetPassword

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(UserResetPassword)
class UserResetPasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'email', 'expiration_time', 'is_confirmation')
    list_display_links = ('id', 'code', 'email')
