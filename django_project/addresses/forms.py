from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address',
            'city',
            'state_province',
            'postal_code',
            'country',
            'phone_number',
            'is_main',
        ]
        labels = {
            'address': 'Indirizzo',
            'city': 'Città',
            'state_province': 'Provincia',
            'postal_code': 'CAP',
            'country': 'Paese',
            'phone_number': 'Numero di Telefono',
            'is_main': 'Imposta come Indirizzo Principale',
        }

        widgets = {
            'is_main': forms.CheckboxInput(
                attrs={'class': 'form-checkbox h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('address', css_class='rounded-pill'),
            Field('city', css_class='rounded-pill'),
            Field('state_province', css_class='rounded-pill'),
            Field('postal_code', css_class='rounded-pill'),
            Field('country', css_class='rounded-pill'),
            Field('phone_number', css_class='rounded-pill'),
        )
