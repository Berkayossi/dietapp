from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from invitations.models import Invitation
from clients.models import Client
from plans.models import Plan

def home(request):
    context = {}
    
    if request.user.is_authenticated:
        if request.user.user_type == 'dietitian':
            # Diyetisyen için dashboard verileri
            context['client_count'] = Client.objects.count()
            context['active_plan_count'] = Plan.objects.filter(is_active=True).count()
            context['pending_invitation_count'] = Invitation.objects.filter(used=False).count()
            
            # Son aktiviteleri al (örnek olarak son 5 davet)
            context['recent_activities'] = [
                f"{inv.email} adresine davet gönderildi - {inv.created_at.strftime('%d/%m/%Y')}"
                for inv in Invitation.objects.order_by('-created_at')[:5]
            ]
            
        elif request.user.user_type == 'client':
            # Müşteri için dashboard verileri
            try:
                client = Client.objects.get(user=request.user)
                context['active_plan'] = Plan.objects.filter(client=client, is_active=True).first()
                # İlerleme verilerini ekle (ileride eklenecek)
                context['progress'] = None
            except Client.DoesNotExist:
                pass
    
    return render(request, 'home.html', context) 