from django.db import models
from recipes.models import Recipe, Favorite
from accounts.models import BMIRecord

# All models have been migrated to their respective apps:
# - accounts.models: UserProfile, BMIRecord
# - recipes.models: Recipe, RecipeStep, Favorite
# - See these apps for the actual model definitions