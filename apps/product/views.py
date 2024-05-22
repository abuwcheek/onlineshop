from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Product, Brand, Category, ProductSize, Size, About, Contact
from django.core.paginator import Paginator
from django.db.models import Q

class HomePageView(View):
    def get(self, request):
        products = Product.objects.all().filter(is_active=True)
        fuatured_products = products.order_by('?')[:16]
        popular_products = products.order_by('?')[:16]
        new_added_product = products.order_by('-created_at')
        new_arrivals_products = products.order_by('-created_at')
        brands = Brand.objects.all().filter(is_active=True)
        monthly_best_sell_featured = products.order_by('-percentage')
        monthly_best_sell_popular = products.order_by('-created_at')
        monthly_best_sell_new_add = products.order_by('-created_at')
        foot_deals_outlet = products.order_by('?')[:3]
        foot_top_selling = products.order_by('?')[:3]
        foot_hot_releases = products.order_by('?')[:3]
        category = Category.objects.all().filter(is_active=True)


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
            'category': category,
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



class ProductDetailView(View):
    def get(self, request, uuid):
        product = get_object_or_404(Product, id=uuid)
        product_color = product.sizes.all().distinct()
        product_sizes = product.sizes.all().values('size').distinct()
        pro_sizes = Size.objects.filter(id__in=product_sizes)
        print(pro_sizes)
        product_comment = product.reviews.all().filter(is_active=True).order_by('?')[:3]

        context = {
            'product': product,
            'product_color': product_color,
            'product_size': pro_sizes,
            'product_comment': product_comment,
        }
        return render(request, 'products/detail.html', context)



class AboutView(View):
    def get(self, request):
        about = About.objects.all()
        context={
            'about': about
        }
        return render(request, 'products/about.html', context)



class ContactView(View):
    def get(self, request):
        contact = Contact.objects.all()
        context = {
            'contact': contact,
        }
        return render(request, 'products/contact.html', context)

    def post(self, request):
        data = request.POST
        if not data.get('first_name'):
            messages.warning(request, "Maydonlar bo'sh bo'lmasligi lozim!")
            return redirect('contact')

        contact = Contact()

        contact.first_name=data.get('first_name')
        contact.email=data.get('email')
        contact.phone=data.get('phone')
        contact.subject=data.get('subject')
        contact.message=data.get('message')

        contact.save()

        messages.success(request, 'Malumotlaringiz yuborildi.')
        return redirect('home')



class SearchView(View):
    def get(self, request):
        query = request.GET.get('query')
        if not query:
            return redirect('home')

        searchs = Product.objects.all().filter(Q(title__icontains = query) | Q(description__icontains = query))
        if not searchs:
            messages.warning(request, 'Siz izlagan mahsulot mavjud emas')
            return redirect('home')

        context = {
            'searchs': searchs,
        }
        messages.success(request, "Siz izlagan mahsulotlar!!!")
        return render(request, 'products/search.html', context)