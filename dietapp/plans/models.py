from django.db import models
from clients.models import Client

class Plan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.client}"

    class Meta:
        verbose_name = "Diyet Planı"
        verbose_name_plural = "Diyet Planları"
        ordering = ['-created_at']

    @property
    def details(self):
        return f"{self.title} ({self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')})"
