from .models import Category


def category_context(request):
     categories = Category.objects.all().filter(is_active=True, parent=None)
     mega_menu = categories[:3]
     last_child_ctg = Category.objects.all().filter(is_active=True, children__isnull=True)
     sevimlilar = 0

     if request.user.is_authenticated:
          sevimlilar = request.user.sevimlilar.all().count()

     context={
          'categories': categories,
          'mega_menu': mega_menu,
          'last_child_ctg': last_child_ctg,
          'sevimlilar': sevimlilar,
     }

     return context