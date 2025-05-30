from django.contrib import admin
from .models import NutritionProgram, Plan
from meals.models import Meal

@admin.register(NutritionProgram)
class NutritionProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_days', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('client', 'program', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'program')
    search_fields = ('client__user__username', 'client__user__email', 'program__title')
    date_hierarchy = 'start_date'
