from django.urls import path
from .views import AddToFavorite, FavoriteView, delete_favorite

urlpatterns = [
     path('add-to-favorite/', AddToFavorite.as_view(), name='add_to_favorite'),
     path('favorite/', FavoriteView.as_view(), name='favorite'),
     path('delete-favorite/<uuid:uuid>/', delete_favorite, name='delete-favorite'),
]