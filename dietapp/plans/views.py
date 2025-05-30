from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import NutritionProgram, Plan
from meals.models import Meal, Food, MealFood
from django.db.models import Q
from clients.models import Client
from .forms import NutritionProgramForm, PlanForm, MealForm, MealFoodFormSet
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

# Create your views here.

@login_required
def my_plans(request):
    """Müşterinin tüm diyet planlarını listeler"""
    plans = Plan.objects.filter(client__user=request.user).order_by('-start_date')
    return render(request, 'plans/my_plans.html', {'plans': plans})

@login_required
def plan_detail(request, plan_id):
    """Belirli bir diyet planının detaylarını gösterir"""
    plan = get_object_or_404(Plan, id=plan_id, client__user=request.user)
    meals = plan.program.meals.all().order_by('day_number', 'time')
    
    # Günlere göre öğünleri grupla
    days = {}
    for meal in meals:
        if meal.day_number not in days:
            days[meal.day_number] = []
        days[meal.day_number].append(meal)
    
    return render(request, 'plans/plan_detail.html', {
        'plan': plan,
        'days': days,
    })

@login_required
def today_meals(request):
    """Bugünün öğünlerini gösterir"""
    today = timezone.now().date()
    
    # Aktif planı bul
    active_plan = Plan.objects.filter(
        client__user=request.user,
        is_active=True,
        start_date__lte=today,
        end_date__gte=today
    ).first()
    
    if not active_plan:
        return render(request, 'plans/today_meals.html', {
            'error': 'Aktif bir diyet planınız bulunmamaktadır.'
        })
    
    # Bugünün öğünlerini bul
    days_passed = (today - active_plan.start_date).days + 1
    meals = active_plan.program.meals.filter(day_number=days_passed).order_by('time')
    
    return render(request, 'plans/today_meals.html', {
        'plan': active_plan,
        'meals': meals,
        'day_number': days_passed
    })

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def nutrition_plans(request):
    """Yönetici için beslenme programları listesi"""
    programs = NutritionProgram.objects.all().order_by('-created_at')
    clients = Client.objects.all()
    
    context = {
        'programs': programs,
        'clients': clients,
        'program_form': NutritionProgramForm(),
        'plan_form': PlanForm()
    }
    
    return render(request, 'plans/nutrition_plans.html', context)

@login_required
@user_passes_test(is_admin)
def create_program(request):
    """Yeni beslenme programı oluşturma"""
    if request.method == 'POST':
        form = NutritionProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, 'Beslenme programı başarıyla oluşturuldu.')
            return redirect('plans:nutrition_plan_detail', program_id=program.id)
    return redirect('plans:nutrition_plans')

@login_required
@user_passes_test(is_admin)
def assign_plan(request):
    """Müşteriye beslenme programı atama"""
    if request.method == 'POST':
        program_id = request.POST.get('program_id')
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.program_id = program_id
            plan.save()
            messages.success(request, 'Program başarıyla müşteriye atandı.')
            return redirect('plans:nutrition_plans')
    return redirect('plans:nutrition_plans')

@login_required
def nutrition_plan_detail(request, program_id):
    program = get_object_or_404(NutritionProgram, id=program_id)
    
    # URL'den gün parametresini al, yoksa 1. günü göster
    current_day = int(request.GET.get('day', 1))
    
    # Gün numarası geçerli mi kontrol et
    if current_day < 1:
        current_day = 1
    elif current_day > program.total_days:
        current_day = program.total_days
    
    # Seçili günün öğünlerini al
    current_day_meals = Meal.objects.filter(
        program=program,
        day_number=current_day
    ).order_by('time')
    
    form = MealForm()
    meal_food_formset = MealFoodFormSet()
    foods = Food.objects.all().order_by('name')
    
    context = {
        'program': program,
        'current_day': current_day,
        'current_day_meals': current_day_meals,
        'form': form,
        'meal_food_formset': meal_food_formset,
        'foods': foods,
    }
    return render(request, 'plans/nutrition_plan_detail.html', context)

@login_required
def get_meal_foods(request, meal_id):
    """Öğüne ait besinleri JSON olarak döndürür."""
    try:
        meal = Meal.objects.get(id=meal_id)
        foods = meal.meal_foods.all()
        data = {
            'foods': [
                {
                    'id': food.food.id,
                    'amount': food.amount
                } for food in foods
            ]
        }
        return JsonResponse(data)
    except Meal.DoesNotExist:
        return JsonResponse({'error': 'Öğün bulunamadı'}, status=404)

@login_required
@user_passes_test(is_admin)
def edit_meal(request, program_id):
    """Öğün düzenleme view'ı."""
    program = get_object_or_404(NutritionProgram, id=program_id)
    
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        try:
            meal = Meal.objects.get(id=meal_id, program=program)
            form = MealForm(request.POST, instance=meal)
            if form.is_valid():
                # Sadece öğün bilgilerini güncelle
                meal = form.save()
                messages.success(request, 'Öğün başarıyla güncellendi.')
                return redirect('plans:meal_detail', meal_id=meal.id)
        except Meal.DoesNotExist:
            messages.error(request, 'Öğün bulunamadı.')
            return redirect('plans:nutrition_plan_detail', program_id=program.id)
    return redirect('plans:nutrition_plan_detail', program_id=program.id)

@login_required
@user_passes_test(is_admin)
def add_meal(request, program_id):
    """Yeni öğün ekleme view'ı."""
    program = get_object_or_404(NutritionProgram, id=program_id)
    
    if request.method == 'POST':
        form = MealForm(request.POST)
        
        if form.is_valid():
            meal = form.save(commit=False)
            meal.program = program
            meal.save()
            
            # Besinleri ekle
            total_forms = int(request.POST.get('meal_food_set-TOTAL_FORMS', 0))
            for i in range(total_forms):
                food_id = request.POST.get(f'meal_food_set-{i}-food')
                amount = request.POST.get(f'meal_food_set-{i}-amount')
                
                if food_id and amount:
                    try:
                        food = Food.objects.get(id=food_id)
                        MealFood.objects.create(
                            meal=meal,
                            food=food,
                            amount=amount
                        )
                    except (Food.DoesNotExist, ValueError):
                        continue
            
            messages.success(request, 'Öğün başarıyla eklendi.')
            return redirect('plans:nutrition_plan_detail', program_id=program.id)
        else:
            messages.error(request, 'Öğün eklenirken bir hata oluştu.')
    
    return redirect('plans:nutrition_plan_detail', program_id=program.id)

@login_required
def meal_detail(request, meal_id):
    # Önce öğünü bul
    meal = get_object_or_404(Meal, id=meal_id)
    
    # Kullanıcının bu öğüne erişim yetkisi var mı kontrol et
    if not (request.user.is_staff or meal.program.plan_set.filter(client__user=request.user).exists()):
        raise PermissionDenied
    
    foods = Food.objects.all().order_by('name')
    
    # Form ve formset oluştur
    form = MealForm(instance=meal)
    meal_food_formset = MealFoodFormSet(instance=meal)
    
    context = {
        'meal': meal,
        'form': form,
        'meal_food_formset': meal_food_formset,
        'foods': foods,
    }
    
    return render(request, 'plans/meal_detail.html', context)

@login_required
def delete_meal_food(request, meal_food_id):
    meal_food = get_object_or_404(MealFood, id=meal_food_id, meal__program__user=request.user)
    
    if request.method == 'POST':
        meal_food.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_admin)
def delete_meal(request, meal_id):
    """Öğün silme view'ı."""
    meal = get_object_or_404(Meal, id=meal_id)
    
    if request.method == 'POST':
        try:
            meal.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False})

@login_required
@user_passes_test(is_admin)
def add_meal_food(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    
    if request.method == 'POST':
        food_id = request.POST.get('food')
        amount = request.POST.get('amount')
        
        try:
            food = Food.objects.get(id=food_id)
            meal_food = MealFood.objects.create(
                meal=meal,
                food=food,
                amount=amount
            )
            return redirect('plans:meal_detail', meal_id=meal.id)
        except (Food.DoesNotExist, ValueError):
            messages.error(request, 'Besin eklenirken bir hata oluştu.')
    
    return redirect('plans:meal_detail', meal_id=meal.id)

@login_required
@user_passes_test(is_admin)
def delete_meal_food(request, meal_food_id):
    meal_food = get_object_or_404(MealFood, id=meal_food_id)
    
    if request.method == 'POST':
        try:
            meal_food.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Geçersiz istek metodu'})
