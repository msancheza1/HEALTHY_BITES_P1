from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('favorite/<int:recipe_id>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:recipe_id>/', views.remove_favorite, name='remove_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
]

#las urls para poner ir a distintas partes dentro de la pagina web