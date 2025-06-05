from django import template
from django.db.models import Sum

register = template.Library()

@register.filter
def sum_calories(meals):
    """Öğünlerin toplam kalorisini hesaplar"""
    return sum(meal.calories for meal in meals)

@register.filter
def sum_protein(meals):
    """Öğünlerin toplam proteinini hesaplar"""
    return round(sum(meal.protein for meal in meals), 1)

@register.filter
def sum_carbs(meals):
    """Öğünlerin toplam karbonhidratını hesaplar"""
    return round(sum(meal.carbs for meal in meals), 1)

@register.filter
def sum_fat(meals):
    """Öğünlerin toplam yağını hesaplar"""
    return round(sum(meal.fat for meal in meals), 1)

@register.simple_tag
def get_range(value):
    """
    Bir sayı verildiğinde 1'den o sayıya kadar olan sayıları döndürür.
    Örnek: 5 verildiğinde [1, 2, 3, 4, 5] döndürür.
    """
    return range(1, int(value) + 1) 