from django.urls import path
from .views import AddToFavorite, FavoriteView, delete_favorite, delete_shop_cart, add_shop_cart, ShopCartView, ShopAddressView, PaymentView

urlpatterns = [
     path('add-to-favorite/', AddToFavorite.as_view(), name='add_to_favorite'),
     path('favorite/', FavoriteView.as_view(), name='favorite'),
     path('delete-favorite/<uuid:uuid>/', delete_favorite, name='delete-favorite'),
     path('delete-shop-cart/<uuid:uuid>/', delete_shop_cart, name='delete-shop-cart'),
     path('add-shop-cart/<uuid:uuid>/', add_shop_cart, name='add-shop-cart'),
     path('shop-cart/', ShopCartView.as_view(), name='shop-cart'),
     path('shop-address/', ShopAddressView.as_view(), name='shop-address'),
     path('payment/<uuid:uuid>/', PaymentView.as_view(), name='payment'),
]