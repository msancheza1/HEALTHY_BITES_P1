from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField(default="No instructions yet")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    vegetarian = models.BooleanField(default=False)
    diabetic_friendly = models.BooleanField(default=False)
    lactose_free = models.BooleanField(default=False)
    gluten_free = models.BooleanField(default=False)
    healthy = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# FR16 — Pasos individuales de cada receta
class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_steps/', blank=True, null=True)  

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.recipe.name} - Step {self.step_number}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"
