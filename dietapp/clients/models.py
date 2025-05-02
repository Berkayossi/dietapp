from django.db import models
from django.conf import settings

# Her müşteriye ait bilgileri tutar. Her müşteri bir kullanıcıdır (CustomUser) ve bir diyetisyene bağlıdır.
class ClientProfile(models.Model):
    # Kullanıcı hesabıyla birebir ilişki (her müşteri bir kullanıcıdır)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Müşterinin bağlı olduğu diyetisyen (diyetisyen de bir kullanıcıdır)
    # Sadece "user_type" = "dietitian" olan kullanıcılar seçilebilir
    dietitian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients',  # diyetisyen.clients.all() ile kendi müşterilerini alabilir
        limit_choices_to={'user_type': 'dietitian'}  # admin arayüzü ve formlarda filtreleme sağlar
    )

    # İsteğe bağlı ek bilgiler
    birth_date = models.DateField(null=True, blank=True)  # doğum tarihi
    notes = models.TextField(blank=True)  # diyetisyenin müşteriyle ilgili notları

    def __str__(self):
        # Admin panelinde ve shell'de görünen temsil
        return f"{self.user.username} - {self.dietitian.username}"


# Müşterinin zamanla ölçülen gelişim verilerini tutar
class ProgressRecord(models.Model):
    # Bu veri hangi müşteriye ait?
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='progress_records')

    # Kayıt tarihi (otomatik olarak oluşturulur)
    date = models.DateField(auto_now_add=True)

    # Gelişim verileri
    weight = models.DecimalField(max_digits=5, decimal_places=2)       # kilo (örnek: 78.50)
    body_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # yağ oranı (%)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)     # bel çevresi (cm)

    # Ek notlar (örneğin: "ölçüm aç karna yapıldı")
    notes = models.TextField(blank=True)

    class Meta:
        # Veriler en güncelden eskiye sıralansın
        ordering = ['-date']

    def __str__(self):
        # Admin ve shell'de anlaşılır gösterim
        return f"{self.client.user.username} - {self.date}"

class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"