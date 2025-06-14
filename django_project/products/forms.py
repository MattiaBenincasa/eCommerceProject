from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Category  # Importa il modello Category


class ProductSearchForm(forms.Form):

    q = forms.CharField(
        label='Cerca Prodotto',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nome del prodotto...'}),
    )

    # Filtro per categoria (checkboxes)
    # queryset=Category.objects.all() popola le opzioni dinamicamente dal database
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Mostra come checkboxes
        required=False,
        label='Seleziona Categoria/e',
    )

    # Campo per l'ordinamento
    SORT_CHOICES = [
        ('', 'Ordina per...'),  # Opzione predefinita
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

    # Filtro per disponibilità (checkbox singola)
    available_only = forms.BooleanField(
        label='Solo Disponibili',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configura Crispy Forms per un layout Bootstrap 5
        self.helper = FormHelper()
        self.helper.form_method = 'get'  # Importante: il form userà il metodo GET per i filtri URL
        self.helper.form_class = 'bg-white p-4 rounded-card shadow-sm mb-4'  # Stile del form

        self.helper.layout = Layout(
            Row(
                Column(Field('q', css_class='form-control-lg'), css_class='col-md-8 mb-3'),
                Column(Submit('submit', 'Cerca', css_class='btn btn-primary btn-lg mt-md-4'),
                       css_class='col-md-4 mb-3 d-flex align-items-center justify-content-end'),
                css_class='align-items-center'
            ),
            Row(
                Column(
                    Field('category', css_class='form-check-inline'),  # Applica classi per checkboxes inline
                    css_class='col-md-6 mb-3'
                ),
                Column(
                    Field('sort_by', css_class='form-select'),  # Stile per il dropdown di selezione
                    css_class='col-md-3 mb-3'
                ),

                Column(
                    # Qui non specifichiamo più il template, lasciando Crispy Forms usare il suo default
                    Field('available_only', css_class='form-check-input'),
                    css_class='col-md-3 mb-3 d-flex align-items-center pt-md-4'
                ),
            )
        )
