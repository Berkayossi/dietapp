from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import InvitationForm
from .models import Invitation

def send_invitation(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit = False)
            invitation.invited_by = request.user  # Burada kullanıcıyı ilişkilendiriyoruz
            invitation.save()
            invite_link = request.build_absolute_uri(f"/invite/{invitation.token}/")

            # E-posta gönderme (geliştirme aşamasında konsola yazılır)
            send_mail(
                subject="Diyet Takip - Davet Linkiniz",
                message=f"Merhaba, kayıt için link: {invite_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[invitation.email],
                fail_silently=False,
            )

            messages.success(request, f"{invitation.email} adresine davet gönderildi.")
            return redirect('send_invitation')
    else:
        form = InvitationForm()
    return render(request, 'invitations/send_invitation.html', {'form': form})

def register_with_token(request, token):
    try:
        invitation = Invitation.objects.get(token=token)
    except Invitation.DoesNotExist:
        return HttpResponse("Geçersiz veya süresi dolmuş davet.", status=400)

    return render(request, 'invitations/register_with_token.html', {'email': invitation.email})
