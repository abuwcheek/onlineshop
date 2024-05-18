from django.shortcuts import render, redirect, get_object_or_404
from .models import Sevimlilar, AddToCardInWishlist, Payment
from django.views import View
from django.contrib import messages
from apps.product.models import Product
from django.db.models import Q
from .forms import PaymentForm
# Create your views here.


class AddToFavorite(View):
     def get(self, request):
          user = request.user
          url = request.META.get('HTTP_REFERER')
          product = request.GET.get('product_id')
          product = Product.objects.get(id=product)
          Sevimlilar.objects.create(user=user, product=product)
          messages.success(request, "Mahsulot sevimlilarga qo'shildi")
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
     messages.success(request, "Mahsulot sevimlilardan o'chirildi")
     return redirect('favorite') 


def add_shop_cart(request, uuid):
     url = request.META.get('HTTP_REFERER')
     user = request.user
     product = Product.objects.get(id=uuid)
     AddToCardInWishlist.objects.create(user=user, product=product)
     messages.success(request, "Mahsulot card ga qo'shildi.")
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
     messages.success(request, "Mahsulot card dan o'chirildi")
     return redirect('shop-cart')



class ShopAddressView(View):
     def get(self, request):
          form = PaymentForm()
          context = {
               'form': form,
          }
          return render(request, 'products/shop-address.html', context)

     def post(self, request):
          
          user = request.user
          orders = AddToCardInWishlist.objects.filter(Q(user=user) & Q(status=False))
          form = PaymentForm(request.POST)
          if form.is_valid():
               payment = form.save(commit=False)
               payment.save()
               payment.order.set(orders)

               return redirect('payment', uuid=payment.id)

          
class PaymentView(View):
     def get(self, request, uuid):
          total = 0
          payment = Payment.objects.get(id=uuid)
          for order in payment.order.all().filter(status = False):
               total += order.product.get_new_price * order.quantity
          context = {
               'total': total,
          }
          return render(request, 'products/cart-totals.html', context)

     def post(self, request, uuid):
          payment = Payment.objects.get(id=uuid)
          for order in payment.order.all():
               order.status = True
               order.save()
               messages.success(request, "Buyurtmangiz Adminga yuborildi.")
          return redirect('shop')