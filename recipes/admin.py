from django.contrib import admin
from .models import Recipe, RecipeStep, Favorite

admin.site.register(Recipe)
admin.site.register(RecipeStep)
admin.site.register(Favorite)
