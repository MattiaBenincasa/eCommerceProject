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


class CheckoutAddressForm(forms.Form):
    existing_addresses = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        empty_label="--- Seleziona un indirizzo ---",
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out',
        }),
        label="Indirizzo di Spedizione"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            user_addresses = Address.objects.filter(user=user)
            self.fields['existing_addresses'].queryset = user_addresses

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'existing_address',
            Submit('submit', 'Conferma Indirizzo', css_class='btn-success mt-3')
        )

