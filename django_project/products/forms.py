from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML, BaseInput
from .models import Product, Category, Review


class CustomSubmit(BaseInput):
    input_type = "submit"
    field_classes = "btn btn-outline-primary"


class ProductSearchForm(forms.Form):

    search_bar = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Cerca qualcosa...'}),
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Seleziona Categoria/e',
    )

    SORT_CHOICES = [
        ('', 'Ordina per...'),
        ('name_asc', 'Nome (A-Z)'),
        ('name_desc', 'Nome (Z-A)'),
        ('price_asc', 'Prezzo (Crescente)'),
        ('price_desc', 'Prezzo (Decrescente)'),
    ]

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label='Ordina per',
    )

    AVAILABILITY_CHOICE = [
        ('', 'Tutti'),
        ('available_only', 'Solo disponibili'),
        ('unavailable_only', 'Solo non disponibili')
    ]

    availability = forms.ChoiceField(
        choices=AVAILABILITY_CHOICE,
        label='Disponibilità',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column(Field('search_bar', css_class='form-control-lg'), css_class='col-md-8'),
                Column(CustomSubmit('submit', 'Cerca', css_class='btn-outline-primary w-100 btn-lg'),
                       css_class='col-md-2 mb-3 d-flex align-items-center'),
                HTML('<div class="col-md-2 mb-3 d-flex align-items-center">'
                        '<button class="btn btn-outline-secondary w-100 btn-lg " type="button" data-bs-toggle="collapse" data-bs-target="#filtersCollapse" aria-expanded="false" aria-controls="filtersCollapse">Filtri</button>'
                     '</div>'),
                css_class='align-items-center'
            ),
            Row(
                Column(
                    Field('category', css_class='form-check-inline'),
                    css_class='col-md-6 mb-3'
                ),
                Column(
                    Field('sort_by', css_class='form-select'),
                    css_class='col-md-3 mb-3'
                ),

                Column(
                    Field('availability', css_class='form-select'),
                    css_class='col-md-3 mb-3'
                ),
                css_class='collapse mt-3',
                id='filtersCollapse'
            )
        )


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Scrivi un titolo per la tua recensione...', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Scrivi qui il tuo commento...'}),
        }
        labels = {
            'title': 'Titolo',
            'message': 'Commento',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('stars', css_class='rounded-md'),
            Field('message', css_class='rounded-md'),
        )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'description',
            'price',
            'stock',
        ]

        labels = {
            'name': 'Nome',
            'category': 'Categoria',
            'description': 'Descrizione',
            'price': 'Prezzo',
            'stock': 'Disponibili',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='rounded-pill'),
            Field('category', css_class='rounded-pill'),
            'description',
            Field('price', css_class='rounded-pill'),
            Field('stock', css_class='rounded-pill'),
            Submit('submit', 'Salva prodotto', css_class='btn btn-success btn-lg rounded-pill w-100 mt-4')
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Nome'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='rounded-pill'),
            Submit('submit', 'Salva', css_class='btn btn-success btn-lg rounded-pill w-100 mt-4')
        )
