from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Food, Meal
import json

@login_required
def food_list(request):
    if request.method == 'POST':
        try:
            data = request.POST
            food = Food.objects.create(
                name=data['name'],
                calories=data['calories'],
                protein=data['protein'],
                fat=data['fat'],
                carbs=data['carbs']
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    foods = Food.objects.all().order_by('name')
    return render(request, 'meals/food_list.html', {'foods': foods})

@login_required
def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    
    if request.method == 'DELETE':
        try:
            food.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            food.name = data.get('name', food.name)
            food.calories = data.get('calories', food.calories)
            food.protein = data.get('protein', food.protein)
            food.fat = data.get('fat', food.fat)
            food.carbs = data.get('carbs', food.carbs)
            food.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({
        'id': food.id,
        'name': food.name,
        'calories': float(food.calories),
        'protein': float(food.protein),
        'fat': float(food.fat),
        'carbs': float(food.carbs)
    })

@login_required
def meal_list(request):
    meals = Meal.objects.filter(user=request.user)
    return render(request, 'meals/meal_list.html', {'meals': meals})

@login_required
def meal_detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    return render(request, 'meals/meal_detail.html', {'meal': meal}) 