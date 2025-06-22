from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Row, Fieldset
from addresses.models import Address


class PaymentForm(forms.Form):
    card_first_name = forms.CharField(
        label='Nome',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nome'})
    )

    card_second_name = forms.CharField(
        label='Cognome',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Cognome'})
    )

    card_number = forms.CharField(
        label='Numero carta',
        max_length=16,
        min_length=16,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'XXXX XXXX XXXX XXXX'})
    )

    expiry_month = forms.CharField(
        label="",
        max_length=2,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'MM'})
    )

    expiry_year = forms.CharField(
        label="",
        max_length=2,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'YY'})
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
            Field('card_first_name', css_class='rounded-pill'),
            Field('card_second_name', css_class='rounded-pill'),
            Field('card_number', css_class='rounded-pill'),
            Fieldset(
                'Data di scadenza',
                Row(
                    Field('expiry_month', css_class='w-25 rounded-pill col-6'),
                    Field('expiry_year', css_class='w-25 rounded-pill col-6'),
                )
            ),
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
