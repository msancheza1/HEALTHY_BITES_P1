from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    height = models.FloatField()
    diabetes = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)

    lactose_intolerant = models.BooleanField(default=False)
    gluten_intolerant = models.BooleanField(default=False)


    def bmi(self):
        return round(self.weight / (self.height ** 2), 2)

    def bmi_category(self):
        bmi_value = self.bmi()

        if bmi_value < 18.5:
            return "underweight"
        elif 18.5 <= bmi_value < 25:
            return "normal"
        else:
            return "overweight"

    def ideal_weight_min(self):
        """Peso mínimo ideal (IMC 18.5) para la altura del usuario"""
        return round(18.5 * (self.height ** 2), 1)

    def ideal_weight_max(self):
        """Peso máximo ideal (IMC 24.9) para la altura del usuario"""
        return round(24.9 * (self.height ** 2), 1)

    def weight_difference(self):
        """Diferencia entre peso actual y rango ideal (negativo = debe subir, positivo = debe bajar)"""
        bmi_value = self.bmi()
        if bmi_value < 18.5:
            return round(self.ideal_weight_min() - self.weight, 1)  # cuánto le falta
        elif bmi_value > 24.9:
            return round(self.weight - self.ideal_weight_max(), 1)  # cuánto le sobra
        else:
            return 0  # está en rango ideal

    def __str__(self):
        return self.user.username



class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField(default="No instructions yet")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)  # NUEVO CAMPO para imagenes
    vegetarian = models.BooleanField(default=False)
    diabetic_friendly = models.BooleanField(default=False)

    lactose_free = models.BooleanField(default=False)   # NUEVO
    gluten_free = models.BooleanField(default=False)    # NUEVO
    
    healthy = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Favorite(models.Model): #definimos lo que conforma una receta favorita
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"