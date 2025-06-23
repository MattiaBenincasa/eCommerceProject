from datetime import date
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Column, Field
from addresses.models import Address
from django.core.validators import RegexValidator


class PaymentForm(forms.Form):
    card_first_name = forms.CharField(
        label='Nome',
        max_length=100,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-ZàèéìòùÀÈÉÌÒÙ' -]+$",
                message='Il nome può contenere solo lettere'
            )
        ],
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nome'})
    )

    card_last_name = forms.CharField(
        label='Cognome',
        max_length=100,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-ZàèéìòùÀÈÉÌÒÙ' -]+$",
                message='Il cognome può contenere solo lettere'
            )
        ],
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Cognome'})
    )

    card_number = forms.CharField(
        label='Numero carta',
        max_length=16,
        min_length=16,
        validators=[
            RegexValidator(
                regex=r'^\d{16}$',
                message='Il numero della carta deve contenere esattamente 16 numeri'
            )
        ],
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'XXXXXXXXXXXXXXXX'})
    )

    expiry_month = forms.CharField(
        label="",
        max_length=2,
        min_length=1,
        validators=[
            RegexValidator(
                regex=r'^0?([1-9]|1[0-2])$',
                message='Inserire un mese valido'
            )
        ],
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'MM'})
    )

    expiry_year = forms.CharField(
        label="",
        max_length=2,
        min_length=2,
        validators=[
          RegexValidator(
              regex=r'^\d{2}$',
              message='Inserire un anno valido'
          )
        ],
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'YY'})
    )

    cvv = forms.CharField(
        label='CVV',
        max_length=3,
        min_length=3,
        validators=[
            RegexValidator(
                regex=r'^\d{3}$',
                message='Inserire un codice numerico di 3 cifre'
            )
        ],
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'XXX'})
    )

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('expiry_month')
        year = cleaned_data.get('expiry_year')

        if month and year:
            try:
                month_int = int(month)
                year_int = int(year) + 2000
            except ValueError:
                raise forms.ValidationError("Formato data di scadenza non valido.")

            current_year = date.today().year
            current_month = date.today().month

            if year_int < current_year:
                self.add_error('expiry_year', 'Carta scaduta anno scorso')
            elif year_int == current_year:
                if month_int <= current_month:
                    self.add_error('expiry_month', "Carta scaduta nell' anno corrente")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'card_first_name',
            'card_last_name',
            'card_number',
            HTML('<div class="form-label requiredField">Data di scadenza*</div>'),
            Row(
                Column('expiry_month', css_class='small_box_input form-group col-md-6 mb-0'),
                HTML('<span class="slash_date">/</span>'),
                Column('expiry_year', css_class='small_box_input form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('cvv', css_class="small_box_input form-group col-md-6 mb-0"),
            Submit('submit', 'Conferma acquisto', css_class='btn btn-success btn-lg rounded-pill w-100 mt-4')
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
