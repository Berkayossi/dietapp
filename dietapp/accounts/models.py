from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('dietitian', 'Diyetisyen'),
        ('client', 'Müşteri'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    # Ortak alanlar burada olabilir, örn: telefon numarası
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def is_dietitian(self):
        return self.user_type == 'dietitian'

    def is_client(self):
        return self.user_type == 'client'
