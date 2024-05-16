from django.shortcuts import render, redirect, get_object_or_404
from .models import Sevimlilar, AddToCardInWishlist
from django.views import View
from apps.product.models import Product
from django.db.models import Q
# Create your views here.


class AddToFavorite(View):
     def get(self, request):
          user = request.user
          url = request.META.get('HTTP_REFERER')
          product = request.GET.get('product_id')
          product = Product.objects.get(id=product)
          Sevimlilar.objects.create(user=user, product=product)
          return redirect(url)

     

class FavoriteView(View):
     def get(self, request):
          user = request.user
          sevimlilar = Sevimlilar.objects.filter(user=user)
          context = {
               'sevimlilar': sevimlilar,
          } 
          return render(request, 'products/shop-wishlist.html', context)

     
def delete_favorite(request, uuid):
     sevimlilar = Sevimlilar.objects.get(id=uuid)
     sevimlilar.delete()
     return redirect('favorite') 


def add_shop_cart(request, uuid):
     url = request.META.get('HTTP_REFERER')
     user = request.user
     product = Product.objects.get(id=uuid)
     AddToCardInWishlist.objects.create(user=user, product=product)
     return redirect(url)



class ShopCartView(View):
     def get(self, request):
          user = request.user
          orders = AddToCardInWishlist.objects.filter(Q(user=user) & Q(status=False))
          context = {
               'orders': orders,
          }
          return render(request, 'products/shop-cart.html', context)



def delete_shop_cart(request, uuid):
     order = AddToCardInWishlist.objects.get(id=uuid)
     order.delete()
     return redirect('shop-cart')



class ShopAddressView(View):
     def get(self, request):
          user = request.user
          orders = AddToCardInWishlist.objects.filter(Q(user=user) & Q(status=False))
          context = {
               'orders': orders,
          }
          return render(request, 'products/shop-address.html', context)