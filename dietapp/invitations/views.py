from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import InvitationForm
from .models import Invitation
from clients.models import Client
from accounts.forms import UserRegistrationForm
from accounts.models import CustomUser

User = get_user_model()

@login_required
def send_invitation(request):
    print("VIEW CALLED!")  # Basit bir print
    if request.method == 'POST':
        print("POST REQUEST RECEIVED!")  # Basit bir print
        form = InvitationForm(request.POST)
        if form.is_valid():
            print("FORM IS VALID!")  # Basit bir print
            invitation = form.save(commit=False)
            invitation.invited_by = request.user
            invitation.save()
            invite_link = request.build_absolute_uri(f"/invitations/{invitation.token}/")

            try:
                print("TRYING TO SEND EMAIL!")  # Basit bir print
                send_mail(
                    subject="Diyet Takip - Davet Linkiniz",
                    message=f"Merhaba, kayıt için link: {invite_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[invitation.email],
                    fail_silently=False,
                )
                print("EMAIL SENT!")  # Basit bir print
            except Exception as e:
                print(f"EMAIL ERROR: {str(e)}")  # Hata mesajı
                messages.error(request, f"E-posta gönderimi başarısız oldu: {str(e)}")
                return redirect('invitations:send_invitation')

            messages.success(request, f"{invitation.email} adresine davet gönderildi.")
            return redirect('invitations:send_invitation')
        else:
            print(f"FORM ERRORS: {form.errors}")  # Form hataları
    else:
        form = InvitationForm()
    return render(request, 'invitations/send_invitation.html', {'form': form})

def invite_register(request, token):
    try:
        invitation = get_object_or_404(Invitation, token=token)
        
        # Token kullanılmış mı kontrol et
        if invitation.used:
            messages.error(request, "Bu davet linki daha önce kullanılmış.")
            return redirect('home')
        
        # Token süresi geçmiş mi kontrol et (24 saat)
        if timezone.now() - invitation.created_at > timedelta(hours=24):
            messages.error(request, "Bu davet linkinin süresi dolmuş.")
            return redirect('home')

    except Invitation.DoesNotExist:
        return HttpResponse("Geçersiz veya süresi dolmuş davet.", status=400)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Kullanıcıyı oluştur ve davetiyeyi işaretle
                user = form.save(invitation=invitation)
                
                # Kullanıcıyı sisteme giriş yaptır
                login(request, user)
                
                # Başarılı mesajını göster
                messages.success(request, "Kayıt işleminiz başarıyla tamamlandı! Hoş geldiniz!")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Kayıt sırasında bir hata oluştu: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'invitations/invite_register.html', {
        'email': invitation.email,
        'form': form
    })

@login_required
def create_invitation(request):
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Bu işlemi yapmak için yetkiniz bulunmuyor.'
        })
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({
                'success': False,
                'error': 'Lütfen bir e-posta adresi girin.'
            })
        
        if Invitation.objects.filter(email=email, used=False).exists():
            return JsonResponse({
                'success': False,
                'error': 'Bu e-posta adresi için zaten aktif bir davetiye bulunuyor.'
            })
        
        invitation = Invitation.objects.create(email=email)
        invite_link = request.build_absolute_uri(f"/invitations/{invitation.token}/")
        
        html_message = render_to_string('invitations/email/invitation_email.html', {
            'invite_link': invite_link,
            'email': email
        })
        
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject="Diyet Takip Sistemi - Davet Linkiniz",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            invitation.delete()
            return JsonResponse({
                'success': False,
                'error': 'Davetiye gönderilemedi. Lütfen daha sonra tekrar deneyin.'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Geçersiz istek.'
    })

@login_required
def resend_invitation(request, token):
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Bu işlemi yapmak için yetkiniz bulunmuyor.'
        })
    
    invitation = get_object_or_404(Invitation, token=token)
    
    if invitation.used:
        return JsonResponse({
            'success': False,
            'error': 'Bu davetiye daha önce kullanılmış.'
        })
        
    invite_link = request.build_absolute_uri(f"/invitations/{invitation.token}/")
    
    html_message = render_to_string('invitations/email/invitation_email.html', {
        'invite_link': invite_link,
        'email': invitation.email
    })
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject="Diyet Takip Sistemi - Davet Linkiniz",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.email],
            html_message=html_message,
            fail_silently=False,
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Davetiye gönderilemedi. Lütfen daha sonra tekrar deneyin.'
        })
