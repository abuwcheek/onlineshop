from .models import Category


def category_context(request):
     categories = Category.objects.all().filter(is_active=True)
     mega_menu = categories.filter(parent__isnull=True)[:3]

     context={
          'categories': categories,
          'mega_menu': mega_menu
     }

     return context