from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from addresses.models import Address


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
