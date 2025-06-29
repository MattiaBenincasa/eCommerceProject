from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Field, HTML, Row, Column
from django.urls import reverse
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, max_length=100, label="Nome")
    last_name = forms.CharField(required=True, max_length=100, label="Cognome")
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}),
                                 label="Data di Nascita")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'birth_date')

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = date.today()
        if (birth_date.year + 18, birth_date.month, birth_date.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Devi essere maggiorenne per poterti registrare')
        return birth_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Crea il tuo Account',
                Field('username', css_class='form-control rounded-md'),
                Field('email', css_class='form-control rounded-md'),
                Field('password1', css_class='form-control rounded-md'),
                Field('password2', css_class='form-control rounded-md'),
                Row(
                    Column(Field('first_name', css_class='form-control rounded-md'), css_class='col-md-6 mb-3'),
                    Column(Field('last_name', css_class='form-control rounded-md'), css_class='col-md-6 mb-3'),
                ),
                Field('birth_date', css_class='form-control rounded-md'),
            ),
            Submit('submit', 'Registrati', css_class='btn btn-primary btn-lg rounded-pill mt-4')
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='form-control rounded-md'),
            Field('password', css_class='form-control rounded-md'),
            Submit('submit', 'Accedi', css_class='btn btn-primary btn-lg rounded-pill mt-4'),
            HTML(f'<p class="text-center mt-3"><a href="{reverse("signup")}" class="text-decoration-none">Non hai un account? Registrati!</a></p>')
        )


class UpdateUserInfoForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='form-control rounded-md'),
            Field('first_name', css_class='form-control rounded-md'),
            Field('last_name', css_class='form-control rounded-md'),
            Field('email', css_class='form-control rounded-md'),
            Submit('submit', 'Conferma', css_class='btn btn-primary btn-lg rounded-pill mt-4'),
        )
