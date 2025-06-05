from django.db import models
from django.conf import settings
from django.utils import timezone
from clients.models import Client

class NutritionProgram(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    diet_type = models.CharField(max_length=50)
    total_days = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_copy = models.BooleanField(default=False, verbose_name="Kopya Program")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Beslenme Programı'
        verbose_name_plural = 'Beslenme Programları'

class Plan(models.Model):
    program = models.ForeignKey(NutritionProgram, on_delete=models.CASCADE, related_name='original_plans')
    program_copy = models.ForeignKey(NutritionProgram, on_delete=models.CASCADE, related_name='copied_plans', null=True, blank=True)
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Aktif'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi')
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.program.title} - {self.client.user.get_full_name() or self.client.user.username}"

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planlar'

    @property
    def is_current(self):
        """Plan şu anda aktif mi kontrol eder"""
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date

    @property
    def remaining_days(self):
        """Kalan gün sayısını hesaplar"""
        today = timezone.now().date()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days

    def save(self, *args, **kwargs):
        """Plan kaydedilirken durum kontrolü yapar"""
        if self.status == 'active':
            # Aynı müşterinin diğer aktif planlarını pasife çek
            Plan.objects.filter(
                client=self.client,
                status='active'
            ).exclude(id=self.id).update(status='completed')
        super().save(*args, **kwargs)
