function sendInvitation(event) {
    event.preventDefault();
    
    const form = document.getElementById('invitationForm');
    const resultDiv = document.getElementById('invitationResult');
    const submitButton = document.getElementById('submitButton');
    const email = document.getElementById('email').value;
    
    // Submit butonunu devre dışı bırak
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Gönderiliyor...';
    
    // Sonuç mesajını temizle
    resultDiv.classList.add('d-none');
    resultDiv.classList.remove('alert-success', 'alert-danger');
    
    fetch('/invitations/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: `email=${encodeURIComponent(email)}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Sunucu hatası: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            resultDiv.classList.remove('d-none');
            resultDiv.classList.add('alert-success');
            resultDiv.textContent = 'Davetiye başarıyla gönderildi!';
            form.reset();
            
            // 2 saniye sonra modalı kapat
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('newInvitationModal'));
                modal.hide();
                // Sayfayı yenile
                window.location.reload();
            }, 2000);
        } else {
            resultDiv.classList.remove('d-none');
            resultDiv.classList.add('alert-danger');
            resultDiv.textContent = data.error;
        }
    })
    .catch(error => {
        resultDiv.classList.remove('d-none');
        resultDiv.classList.add('alert-danger');
        resultDiv.textContent = error.message;
    })
    .finally(() => {
        // Submit butonunu tekrar aktif et
        submitButton.disabled = false;
        submitButton.textContent = 'Davetiye Gönder';
    });
    
    return false;
}

function resendInvitation(token) {
    if (confirm('Davetiyeyi tekrar göndermek istediğinizden emin misiniz?')) {
        fetch(`/invitations/${token}/resend/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Sunucu hatası: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Davetiye başarıyla tekrar gönderildi!');
                // Sayfayı yenile
                window.location.reload();
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            alert(error.message);
        });
    }
} 