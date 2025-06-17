from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class PaymentForm(forms.Form):
    card_first_name = forms.CharField(
        label='Nome',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nome e Cognome'})
    )

    card_second_name = forms.CharField(
        label='Cognome',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nome e Cognome'})
    )

    card_number = forms.CharField(
        label='Numero carta',
        max_length=16,
        min_length=16,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'XXXX XXXX XXXX XXXX'})
    )

    expiry_date = forms.CharField(
        label='Data di scadenza (MM/AA)',
        max_length=5,
        min_length=5,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'MM/AA'})
    )
    cvv = forms.CharField(
        label='CVV',
        max_length=3,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'XXX'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('Nome', css_class='rounded-pill'),
            Field('Cognome', css_class='rounded-pill'),
            Field('Numero Carta', css_class='rounded-pill'),
            Field('Data di scadenza', css_class='rounded-pill'),
            Field('cvv', css_class='rounded-pill'),
        )
