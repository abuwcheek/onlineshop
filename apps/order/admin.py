from django.contrib import admin
from .models import Sevimlilar, AddToCardInWishlist, Payment
# Register your models here.



@admin.register(Sevimlilar)
class SevimlilarAdmin(admin.ModelAdmin):
     list_display = ['user', 'product']
     list_display_links = ['user', 'product']
     search_fields = ['user', 'product']
     list_per_page = 10
     

@admin.register(AddToCardInWishlist)
class AddToCardInWishlistAdmin(admin.ModelAdmin):
     list_display = ['user', 'product', 'quantity']
     list_display_links = ['user', 'product']
     search_fields = ['user', 'product']
     list_per_page = 10


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
     list_display = ['country','address','phone','total', 'created_at',]
     list_display_links = ['country','address']
     list_filter = ['country']
     search_fields = ['country']
     list_per_page = 10