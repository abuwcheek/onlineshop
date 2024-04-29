from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product, Brand, Category
from django.core.paginator import Paginator
from django.db.models import Q

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


class ShopAllView(View):
    def get(self, request):

        sort_by = request.GET.get('sort_by', '?')

        shop_product = Product.objects.all().filter(is_active=True).order_by(sort_by)
        categories = Category.objects.all().filter(is_active=True, parent=None)

        page_size = request.GET.get('page_size', 10)
        if page_size == 'all':
            page_size = shop_product.count()


        paginator = Paginator(shop_product, page_size)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)



        new_product = shop_product.order_by('-created_at')[:3]

        
        context = {
            'shop_product': page_obj,
            'page_size': page_size,
            'categories': categories,
            'new_product': new_product,
        }
        return render(request, 'products/shop.html', context)



class ShopCategoryView(View):
    def get(self, request, uuid):
        ctg = get_object_or_404(Category, id=uuid)
        categories = Category.objects.all().filter(is_active=True, parent=ctg)
        if not categories:
            categories = Category.objects.all().filter(is_active=True, level=1)

        ctg_products = ctg.products.filter(is_active=True).order_by('?')

        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(ctg_products, page_size)

        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        


        context = {
            'shop_product': page_obj,
            'page_size': page_size,
            'categories': categories, 
        }
        return render(request, 'products/shop.html', context)



class SearchView(View):
    def get(self, request):
        query = request.GET.get('search')
        if not query:
            searchs = Product.objects.all().order_by('-created_at')
        else:
            searchs = Product.objects.all().filter(Q(title__icontains = query) | Q(description__icontains = query))

        context = {
            'searchs': searchs,
        }

        return render(request, 'products/shop.html', context)