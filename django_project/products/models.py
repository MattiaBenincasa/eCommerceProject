from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name="Nome Categoria")
    slug = models.SlugField(max_length=100, unique=True, help_text="Slug unico per l'URL della categoria")

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categorie"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome Prodotto")
    slug = models.SlugField(max_length=200, unique=True, help_text="Slug unico per l'URL del prodotto")

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"slug": self.slug})
