from django.contrib import admin
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at')
    readonly_fields = ('token', 'created_at')

    def has_change_permission(self, request, obj=None):
        # Var olan davetiyeleri değiştirmeyi engelle
        return False

    def has_delete_permission(self, request, obj=None):
        # Silinmesine de gerek yok şimdilik
        return False