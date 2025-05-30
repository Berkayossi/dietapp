from django.contrib import admin
from .models import Food, Meal, MealFood

class MealFoodInline(admin.TabularInline):
    model = MealFood
    extra = 1
    fields = ('food', 'amount')

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'fat', 'carbs')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'meal_type', 'day_number', 'time')
    list_filter = ('meal_type', 'program')
    search_fields = ('name', 'description')
    ordering = ('day_number', 'time')
    inlines = [MealFoodInline]

@admin.register(MealFood)
class MealFoodAdmin(admin.ModelAdmin):
    list_display = ('meal', 'food', 'amount', 'calories', 'protein', 'fat', 'carbs')
    list_filter = ('meal__program', 'meal__meal_type')
    search_fields = ('meal__name', 'food__name') 