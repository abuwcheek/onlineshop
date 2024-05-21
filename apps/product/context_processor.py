from .models import Category, Brand, About, Product


def category_context(request):
     categories = Category.objects.all().filter(is_active=True, parent=None)
     mega_menu = categories[:3]
     last_child_ctg = Category.objects.all().filter(is_active=True, children__isnull=True)
     brands = Brand.objects.all().filter(is_active=True)
     about = About.objects.first()
     lastes_product = Product.objects.all().filter(is_active=True).order_by('-created_at')[:4]
     sevimlilar = 0
     cards = 0

     if request.user.is_authenticated:
          sevimlilar = request.user.sevimlilar.all().count()
          cards = request.user.orders.all().filter(status=False).count()

     context={
          'categories': categories,
          'mega_menu': mega_menu,
          'last_child_ctg': last_child_ctg,
          'sevimlilar': sevimlilar,
          'cards': cards,
          'brands': brands,
          'about': about,
          'lastes_product': lastes_product,
     }

     return context