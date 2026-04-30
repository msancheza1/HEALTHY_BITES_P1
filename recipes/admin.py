
from django.contrib import admin
from .models import Recipe, RecipeStep, Favorite

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeStepInline]

admin.site.register(Favorite)