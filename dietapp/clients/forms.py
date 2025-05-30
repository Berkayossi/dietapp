from django import forms
from .models import ProgressRecord

class ProgressRecordForm(forms.ModelForm):
    class Meta:
        model = ProgressRecord
        fields = ['date', 'weight', 'body_fat', 'waist', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'body_fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'waist': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 