from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from invitations.models import Invitation
from clients.models import Client
from plans.models import Plan

CustomUser = get_user_model()

def home(request):
    context = {}
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Yönetici için dashboard verileri
            context['client_count'] = Client.objects.count()
            context['active_plan_count'] = Plan.objects.filter(is_active=True).count()
            context['pending_invitation_count'] = Invitation.objects.filter(used=False).count()
            context['active_client_count'] = CustomUser.objects.filter(is_active=True, is_staff=False).count()
            
            # Davetiye listesini ekle
            context['invitations'] = Invitation.objects.all().order_by('-created_at')
            
            # Son aktiviteleri al (örnek olarak son 5 davet)
            context['recent_activities'] = [
                f"{inv.email} adresine davet gönderildi - {inv.created_at.strftime('%d/%m/%Y')}"
                for inv in Invitation.objects.order_by('-created_at')[:5]
            ]
            
            context['is_admin'] = True
            return render(request, 'dashboard/admin_dashboard.html', context)
            
        elif request.user.user_type == 'dietitian':
            # Diyetisyen için dashboard verileri
            context['client_count'] = Client.objects.count()
            context['active_plan_count'] = Plan.objects.filter(is_active=True).count()
            context['pending_invitation_count'] = Invitation.objects.filter(used=False).count()
            
            # Son aktiviteleri al (örnek olarak son 5 davet)
            context['recent_activities'] = [
                f"{inv.email} adresine davet gönderildi - {inv.created_at.strftime('%d/%m/%Y')}"
                for inv in Invitation.objects.order_by('-created_at')[:5]
            ]
            
            return render(request, 'dashboard/dietitian_dashboard.html', context)
            
        elif request.user.user_type == 'client':
            # Müşteri için dashboard verileri
            try:
                client = Client.objects.get(user=request.user)
                context['active_plan'] = Plan.objects.filter(client=client, is_active=True).first()
                # İlerleme verilerini ekle (ileride eklenecek)
                context['progress'] = None
            except Client.DoesNotExist:
                pass
            
            return render(request, 'dashboard/client_dashboard.html', context)
    
    return render(request, 'home.html', context) 