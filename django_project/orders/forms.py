from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import Order


class MyOrderFilter(forms.Form):
    order_number = forms.CharField(
        max_length=10,
        required=False,
        label="Numero Ordine",
        widget=forms.TextInput(attrs={'placeholder': 'Es. 123'})
    )

    status_filter = forms.ChoiceField(
        choices=[
            ('', 'Tutti'),
            ('Delivered', 'Consegnati'),
            ('Cancelled', 'Annullati'),
            ('Shipped', 'Spediti'),
            ('Processing', 'In lavorazione'),
        ],
        required=False,
        label="Filtra per Stato di consegna",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    SORT_CHOICES = [
        ('', 'Ordina per...'),
        ('latest', 'Ordini più recenti'),
        ('earliest', 'Ordini più vecchi'),
    ]

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label='Ordina per',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = ''

        self.helper.layout = Layout(
            Row(
                Column('order_number', css_class='col-md-1 mb-0'),
                Column('sort_by', css_class='col-md-2 mb-0'),
                Column('status_filter', css_class='col-md-2 mb-0'),
                css_class='g-3 align-items-end'
            ),
            Row(
                Column(
                    Submit('submit', 'Applica Filtri', css_class='btn btn-primary h-100'),
                    css_class='col-md-2 d-grid align-self-end mb-0'),
                css_class='g-3 align-items-end'
            ),
        )


class OrderFilterForm(forms.Form):
    date_filter = forms.ChoiceField(
        choices=[
            ('', 'Tutti'),
            ('today', 'Oggi'),
            ('last_week', 'Ultima Settimana'),
            ('last_month', 'Ultimo Mese'),
        ],
        required=False,
        label="Filtra per Data",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    customer_query = forms.CharField(
        max_length=100,
        required=False,
        label="Ricerca Cliente (Nome/Cognome/Username)",
        widget=forms.TextInput(attrs={'placeholder': 'Es. Rossi'})
    )
    order_number = forms.CharField(
        max_length=10,
        required=False,
        label="Numero Ordine",
        widget=forms.TextInput(attrs={'placeholder': 'Es. 123'})
    )

    status_filter = forms.ChoiceField(
        choices=[
            ('', 'Tutti'),
            ('Delivered', 'Consegnati'),
            ('Cancelled', 'Annullati'),
            ('Shipped', 'Spediti'),
            ('Processing', 'In lavorazione'),
        ],
        required=False,
        label="Filtra per Stato di consegna",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    SORT_CHOICES = [
        ('', 'Ordina per...'),
        ('latest', 'Ordini più recenti'),
        ('earliest', 'Ordini più vecchi'),
    ]

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label='Ordina per',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = ''

        self.helper.layout = Layout(
            Row(
                Column('customer_query', css_class='col-md-3 mb-0'),
                Column('order_number', css_class='col-md-1 mb-0'),
                Column('date_filter', css_class='col-md-2 mb-0'),
                Column('sort_by', css_class='col-md-2 mb-0'),
                Column('status_filter', css_class='col-md-2 mb-0'),
                css_class='g-3 align-items-end'
            ),
            Row(
                Column(
                    Submit('submit', 'Applica Filtri', css_class='btn btn-primary h-100'),
                    css_class='col-md-2 d-grid align-self-end mb-0'),
                css_class='g-3 align-items-end'
            ),
            HTML('<div class="col-md-12 d-grid mt-2"><a href="{% url \'customers_orders\' %}" class="btn btn-outline-secondary">Reset Filtri</a></div>')
        )


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'status',
            Submit('submit', 'Aggiorna Stato', css_class='btn btn-success mt-3')
        )
