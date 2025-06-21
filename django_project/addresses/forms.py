from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
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
            'phone_number': 'Numero di Telefono (Opzionale)',
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
            Row(
                Column('address', css_class='md:w-1/2'),
                css_class='flex flex-wrap -mx-3 mb-6'
            ),
            Row(
                Column('city', css_class='md:w-1/3'),
                Column('state_province', css_class='md:w-1/3'),
                Column('postal_code', css_class='md:w-1/3'),
                css_class='flex flex-wrap -mx-3 mb-6'
            ),
            Row(
                Column('phone_number', css_class='md:w-1/2'),
                css_class='flex flex-wrap -mx-3 mb-6'
            ),
            'country',  # Campo singolo a tutta larghezza
            'is_main',  # Checkbox
            Submit('submit', 'Salva Indirizzo',
                   css_class='bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-md shadow-md transition duration-300')
        )
        # Aggiunge classi Tailwind predefinite a tutti i campi se non specificato altrimenti
        for field in self.fields:
            if field != 'is_main':  # Escludi il checkbox
                self.fields[field].widget.attrs.update({
                                                           'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'})