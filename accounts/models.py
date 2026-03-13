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
        return round(18.5 * (self.height ** 2), 1)

    def ideal_weight_max(self):
        return round(24.9 * (self.height ** 2), 1)

    def weight_difference(self):
        bmi_value = self.bmi()
        if bmi_value < 18.5:
            return round(self.ideal_weight_min() - self.weight, 1)
        elif bmi_value > 24.9:
            return round(self.weight - self.ideal_weight_max(), 1)
        else:
            return 0

    def __str__(self):
        return self.user.username


# FR21 — Historial de progreso BMI
# Se guarda un snapshot cada vez que el usuario guarda su perfil
class BMIRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bmi_records')
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()
    category = models.CharField(max_length=20)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.user.username} — BMI {self.bmi} ({self.recorded_at.date()})"
