from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:id>/steps/', views.recipe_steps, name='recipe_steps'),
    path('favorite/<int:recipe_id>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:recipe_id>/', views.remove_favorite, name='remove_favorite'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('search/', views.search, name='search'),
]
