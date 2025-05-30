from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Client, ProgressRecord
from .forms import ProgressRecordForm

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def client_list(request):
    """Yönetici için müşteri listesi"""
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'clients/client_list.html', {'clients': clients})

@login_required
@user_passes_test(is_admin)
def client_detail(request, client_id):
    """Müşteri detay sayfası"""
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        form = ProgressRecordForm(request.POST)
        if form.is_valid():
            progress_record = form.save(commit=False)
            progress_record.client = client
            progress_record.save()
            messages.success(request, 'İlerleme kaydı başarıyla eklendi.')
            return redirect('clients:client_detail', client_id=client.id)
    else:
        form = ProgressRecordForm()
    
    context = {
        'client': client,
        'form': form,
    }
    return render(request, 'clients/client_detail.html', context)
