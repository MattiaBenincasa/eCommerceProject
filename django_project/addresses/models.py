from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Italia")
    phone_number = models.CharField(max_length=20)
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Indirizzo"
        verbose_name_plural = "Indirizzi"
        ordering = ['-is_main', 'city']

    def __str__(self):
        return f'{self.city} ({self.state_province}), {self.address}'


# Uso un signal pre_save per gestire l'unicità dell'indirizzo predefinito
# Ogni utente ha un unico indirizzo predefinito

@receiver(pre_save, sender=Address)
def set_unique_default_address(sender, instance, **kwargs):
    if instance.is_main:
        Address.objects.filter(
            user=instance.user,
            is_main=True
        ).exclude(pk=instance.pk).update(is_main=False)
    else:
        pass
