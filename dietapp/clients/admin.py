from django.contrib import admin
from .models import ClientProfile, ProgressRecord, Client

# ClientProfile modeli admin panelinde görüntülenirken ekstra bilgiler göstereceğiz
@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dietitian', 'birth_date')  # listede gözüken alanlar
    search_fields = ('user__username', 'dietitian__username')  # arama yapılabilir alanlar
    list_filter = ('dietitian',)


# ProgressRecord modeli için admin ayarları
@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'weight', 'body_fat', 'waist')  # kayıt listesi görünümü
    search_fields = ('client__user__username',)
    list_filter = ('date',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('created_at',)
