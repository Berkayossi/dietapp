from django.db import models
from django.conf import settings
from clients.models import Client

class NutritionProgram(models.Model):
    """Genel beslenme programı şablonu"""
    title = models.CharField(max_length=100, verbose_name="Program Adı")
    description = models.TextField(verbose_name="Açıklama")
    total_days = models.PositiveIntegerField(verbose_name="Toplam Gün")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Beslenme Programı"
        verbose_name_plural = "Beslenme Programları"
        ordering = ['-created_at']

class Plan(models.Model):
    """Müşteriye atanan beslenme programı"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Müşteri")
    program = models.ForeignKey(NutritionProgram, on_delete=models.CASCADE, verbose_name="Program")
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(verbose_name="Bitiş Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.program}"

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planlar"
        ordering = ['-start_date']

    @property
    def details(self):
        return f"{self.program.title} ({self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')})"
