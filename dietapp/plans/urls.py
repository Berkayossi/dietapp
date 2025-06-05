from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('nutrition-plans/', views.nutrition_plans, name='nutrition_plans'),
    path('nutrition-plans/create/', views.create_program, name='create_program'),
    path('nutrition-plans/assign/', views.assign_plan, name='assign_plan'),
    path('nutrition-plans/<int:program_id>/', views.nutrition_plan_detail, name='nutrition_plan_detail'),
    path('nutrition-plans/<int:program_id>/add-meal/', views.add_meal, name='add_meal'),
    path('nutrition-plans/<int:program_id>/edit-meal/', views.edit_meal, name='edit_meal'),
    path('get-meal-foods/<int:meal_id>/', views.get_meal_foods, name='get_meal_foods'),
    path('my-plans/', views.my_plans, name='my_plans'),
    path('my-plans/<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('today-meals/', views.today_meals, name='today_meals'),
    path('meal/<int:meal_id>/', views.meal_detail, name='meal_detail'),
    path('add-meal-food/<int:meal_id>/', views.add_meal_food, name='add_meal_food'),
    path('delete-meal-food/<int:meal_food_id>/', views.delete_meal_food, name='delete_meal_food'),
    path('delete-meal/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path('delete/', views.delete_program, name='delete_program'),
] 