from django.contrib import admin
from .models import UserProfile, Recipe

admin.site.register(UserProfile)
admin.site.register(Recipe)

from .models import Favorite
admin.site.register(Favorite)