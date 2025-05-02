from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'client__user__username', 'description')
    date_hierarchy = 'start_date'
