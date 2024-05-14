from django.shortcuts import render, redirect, get_object_or_404
from .models import Sevimlilar
from django.views import View
from apps.product.models import Product
# Create your views here.


class AddToFavorite(View):
     def post(self, request):
          user = request.user
          product = request.POST.get('product_id')
          product = Product.objects.get(id=product)
          Sevimlilar.objects.create(user=user, product=product)
          return redirect('detail', uuid=product.id)

     

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