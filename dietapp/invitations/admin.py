from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at', 'used')
    readonly_fields = ('token', 'created_at')

    def has_change_permission(self, request, obj=None):
        # Var olan davetiyeleri değiştirmeyi engelle
        return False

    def has_delete_permission(self, request, obj=None):
        # Silinmesine de gerek yok şimdilik
        return False

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None  # Yeni kayıt mı kontrol et
        super().save_model(request, obj, form, change)
        
        # Sadece yeni kayıtlar için e-posta gönder
        if is_new:
            print("YENİ DAVET OLUŞTURULDU - E-POSTA GÖNDERİLİYOR")
            invite_link = request.build_absolute_uri(f"/invitations/{obj.token}/")
            try:
                send_mail(
                    subject="Diyet Takip - Davet Linkiniz",
                    message=f"Merhaba, kayıt için link: {invite_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    fail_silently=False,
                )
                print(f"E-POSTA GÖNDERİLDİ: {obj.email}")
            except Exception as e:
                print(f"E-POSTA HATASI: {str(e)}")
                raise Exception(f"E-posta gönderilemedi: {str(e)}")