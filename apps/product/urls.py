from django.urls import path
from .views import HomePageView, ShopAllView, ShopCategoryView, ProductDetailView, SearchView, AboutView, ContactView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('shop/', ShopAllView.as_view(), name="shop"),
    path('shop/<uuid:uuid>/', ShopCategoryView.as_view(), name="shop"),
    path('product/<uuid:uuid>/', ProductDetailView.as_view(), name="detail"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('search/', SearchView.as_view(), name="search"),
]