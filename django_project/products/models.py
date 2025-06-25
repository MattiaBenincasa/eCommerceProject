from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from autoslug import AutoSlugField


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name="Nome Categoria")
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categorie"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome Prodotto")
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Categoria"
    )

    description = models.TextField(verbose_name="Descrizione prodotto")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prezzo in €"
    )
    stock = models.IntegerField(
        default=0,
        verbose_name="Quantità Disponibile",
        help_text="Quantità di prodotti disponibili in magazzino."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data Creazione")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ultimo Aggiornamento")

    class Meta:
        ordering = ('name',)
        verbose_name = "Prodotto"
        verbose_name_plural = "Prodotti"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"slug": self.slug})


class Review(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'product')
