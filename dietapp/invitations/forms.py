from django import forms
from django.contrib.auth import get_user_model
from .models import Invitation

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Şifre', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Şifre (Tekrar)', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Şifreler eşleşmiyor.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user