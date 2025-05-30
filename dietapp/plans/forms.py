from django import forms
from .models import NutritionProgram, Plan
from meals.models import Meal, MealFood

class NutritionProgramForm(forms.ModelForm):
    class Meta:
        model = NutritionProgram
        fields = ['title', 'description', 'total_days', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['client', 'program', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MealFoodForm(forms.ModelForm):
    class Meta:
        model = MealFood
        fields = ['food', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '0', 'step': '0.1'}),
        }

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_type', 'name', 'description', 'day_number', 'time']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

MealFoodFormSet = forms.inlineformset_factory(
    Meal, MealFood,
    form=MealFoodForm,
    extra=1,
    can_delete=True
) 