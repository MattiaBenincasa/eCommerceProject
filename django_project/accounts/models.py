from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'birth_date']

    class Meta:
        permissions = [
            ('can_access_manager_dashboard', 'Può accedere alla dashboard degli store manager'),
            ('can_access_customer_dashboard', 'Può accedere alla dashboard clienti')
        ]

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


