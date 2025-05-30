from django.db import models
from django.conf import settings

class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name="Besin Adı")
    calories = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Kalori (kcal/100g)")
    protein = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Protein (g/100g)")
    fat = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Yağ (g/100g)")
    carbs = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Karbonhidrat (g/100g)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Besin"
        verbose_name_plural = "Besinler"
        ordering = ['name']

    def __str__(self):
        return self.name

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Kahvaltı'),
        ('lunch', 'Öğle Yemeği'),
        ('dinner', 'Akşam Yemeği'),
        ('snack', 'Ara Öğün'),
    ]

    program = models.ForeignKey('plans.NutritionProgram', on_delete=models.CASCADE, related_name='meals')
    name = models.CharField(max_length=100, verbose_name="Öğün Adı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, verbose_name="Öğün Tipi")
    day_number = models.PositiveIntegerField(verbose_name="Gün")
    time = models.TimeField(verbose_name="Saat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def calories(self):
        """Öğündeki toplam kalori miktarını hesaplar"""
        total = 0
        for meal_food in self.meal_foods.all():
            food = meal_food.food
            amount = meal_food.amount
            # 100g üzerinden hesapla
            total += (food.calories * amount) / 100
        return round(total)

    @property
    def protein(self):
        """Öğündeki toplam protein miktarını hesaplar"""
        total = 0
        for meal_food in self.meal_foods.all():
            food = meal_food.food
            amount = meal_food.amount
            total += (food.protein * amount) / 100
        return round(total, 1)

    @property
    def carbs(self):
        """Öğündeki toplam karbonhidrat miktarını hesaplar"""
        total = 0
        for meal_food in self.meal_foods.all():
            food = meal_food.food
            amount = meal_food.amount
            total += (food.carbs * amount) / 100
        return round(total, 1)

    @property
    def fat(self):
        """Öğündeki toplam yağ miktarını hesaplar"""
        total = 0
        for meal_food in self.meal_foods.all():
            food = meal_food.food
            amount = meal_food.amount
            total += (food.fat * amount) / 100
        return round(total, 1)

    class Meta:
        verbose_name = "Öğün"
        verbose_name_plural = "Öğünler"
        ordering = ['day_number', 'time']
        unique_together = ['program', 'day_number', 'time']

    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.name}"

class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meal_foods')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="Besin")
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Miktar (g)")

    @property
    def calories(self):
        return (self.food.calories * self.amount) / 100

    @property
    def protein(self):
        return (self.food.protein * self.amount) / 100

    @property
    def fat(self):
        return (self.food.fat * self.amount) / 100

    @property
    def carbs(self):
        return (self.food.carbs * self.amount) / 100

    class Meta:
        verbose_name = "Öğün Besini"
        verbose_name_plural = "Öğün Besinleri" 