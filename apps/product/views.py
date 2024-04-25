from django.shortcuts import render
from django.views import View
from .models import Product, Brand


class HomePageView(View):
    def get(self, request):
        products = Product.objects.all().filter(is_active=True)
        fuatured_products = products.order_by('?')[:16]
        popular_products = products.order_by('?')[:16]
        new_added_product = products.order_by('-created_at')
        new_arrivals_products = products.order_by('-updated_at')
        brands = Brand.objects.all().filter(is_active=True)
        monthly_best_sell_featured = products.order_by('-percentage')
        monthly_best_sell_popular = products.order_by('-created_at')
        monthly_best_sell_new_add = products.order_by('-created_at')
        foot_deals_outlet = products.order_by('?')[:3]
        foot_top_selling = products.order_by('?')[:3]
        foot_hot_releases = products.order_by('?')[:3]

        context = {
            'products': products,
            'fuatured_products': fuatured_products,
            'popular_products': popular_products,
            'new_added_product': new_added_product,
            'new_arrivals_products' : new_arrivals_products,
            'brands': brands,
            'monthly_best_sell_products': monthly_best_sell_featured,
            'monthly_best_sell_popular': monthly_best_sell_popular,
            'monthly_best_sell_new_add': monthly_best_sell_new_add,
            'foot_deals_outlet': foot_deals_outlet,
            'foot_top_selling': foot_top_selling,
            'foot_hot_releases': foot_hot_releases,
        }
        return render(request, 'products/index.html', context)


