from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at', 'used')
    readonly_fields = ('token', 'created_at')
    search_fields = ('email',)
    list_filter = ('used', 'created_at')
    ordering = ('-created_at',)

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
            invite_link = request.build_absolute_uri(f"/invitations/{obj.token}/")
            
            # HTML email template
            html_message = render_to_string('invitations/email/invitation_email.html', {
                'invite_link': invite_link,
                'email': obj.email
            })
            
            # Plain text version
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(
                    subject="Diyet Takip Sistemi - Davet Linkiniz",
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                self.message_user(request, f"Davetiye başarıyla gönderildi: {obj.email}")
            except Exception as e:
                self.message_user(request, f"E-posta gönderilirken hata oluştu: {str(e)}", level='error')
                raise Exception(f"E-posta gönderilemedi: {str(e)}")