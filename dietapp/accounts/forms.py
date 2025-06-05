from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from clients.models import Client

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=True, label='Telefon Numarası')
    birth_date = forms.DateField(required=True, label='Doğum Tarihi', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'password1', 'password2')

    def save(self, commit=True, invitation=None):
        user = super().save(commit=False)
        # Eğer davet varsa, e-posta adresini davetiyeden al
        user.email = invitation.email if invitation else self.cleaned_data.get('email', '')
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = 'client'  # Tüm kayıt olan kullanıcılar client olarak ayarlanıyor
        
        if commit:
            user.save()
            # Client modelini oluştur
            Client.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                birth_date=self.cleaned_data['birth_date']
            )
            
            # Eğer davet varsa, davetiyeyi kullanıldı olarak işaretle
            if invitation:
                invitation.used = True
                invitation.save()
                
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email') 