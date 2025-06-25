import re

from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=2,
                                      validators=[
                                          RegexValidator(
                                              regex=r'^[a-z]{2}$',
                                              message='Inserire la sigla delle provincia',
                                              flags=re.IGNORECASE
                                          )
                                      ])
    postal_code = models.CharField(max_length=5,
                                   validators=[
                                       RegexValidator(
                                           regex=r'^\d{5}$',
                                           message='Inserire un CAP valido (5 cifre)'
                                       )
                                   ]
                                   )
    country = models.CharField(max_length=100, default="Italia")
    phone_number = models.CharField(max_length=15,
                                    validators=[
                                        RegexValidator(
                                            regex=r'^\d{1,'
                                                  r'15}$',
                                            message='Inserisci un numero di telefono italiano'
                                        )
                                    ]
                                    )
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Indirizzo"
        verbose_name_plural = "Indirizzi"
        ordering = ['-is_main', 'city']
        permissions = [
            ('can_select_address_in_checkout', 'Può selezionare indirizzo nel checkout'),
        ]

    def save(self, *args, **kwargs):
        if self.is_main:
            Address.objects.filter(user=self.user, is_main=True).exclude(pk=self.pk).update(is_main=False)
        elif not self.is_main and not Address.objects.filter(user=self.user).exclude(pk=self.pk):
            self.is_main = True

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_main and Address.objects.filter(user=self.user).exclude(pk=self.pk):
            new_main_address = Address.objects.filter(user=self.user).exclude(pk=self.pk).first()
            new_main_address.is_main = True
            new_main_address.save()
        else:
            pass
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.city} ({self.state_province}), {self.address}'
