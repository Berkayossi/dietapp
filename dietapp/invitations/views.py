from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .forms import InvitationForm
from .models import Invitation

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
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Şifreler eşleşmiyor.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış.")
        else:
            try:
                # Kullanıcıyı oluştur
                user = User.objects.create_user(
                    username=username,
                    email=invitation.email,
                    password=password1,
                    user_type='client'  # Davet edilen kullanıcılar client olarak ayarlanıyor
                )
                
                # Davetiyeyi kullanıldı olarak işaretle
                invitation.used = True
                invitation.save()
                
                # Kullanıcıyı sisteme giriş yaptır
                login(request, user)
                
                # Başarılı mesajını göster
                messages.success(request, "Kayıt işleminiz başarıyla tamamlandı! Hoş geldiniz!")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Kayıt sırasında bir hata oluştu: {str(e)}")

    return render(request, 'invitations/invite_register.html', {'email': invitation.email})
