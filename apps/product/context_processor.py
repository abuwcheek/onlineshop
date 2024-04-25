from .models import Category


def category_context(request):
     categories = Category.objects.all().filter(is_active=True, parent=None)
     mega_menu = categories[:3]
     last_child_ctg = Category.objects.all().filter(is_active=True, children__isnull=True)

     context={
          'categories': categories,
          'mega_menu': mega_menu,
          'last_child_ctg': last_child_ctg,
     }

     return context