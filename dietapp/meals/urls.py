from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('foods/', views.food_list, name='food_list'),
    path('foods/<int:pk>/', views.food_detail, name='food_detail'),
    path('meals/', views.meal_list, name='meal_list'),
    path('meals/<int:pk>/', views.meal_detail, name='meal_detail'),
] 