from django.shortcuts import render
from django.views import View
from .models import Product


class HomePageView(View):
    def get(self, request):
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'products/index.html', context)
