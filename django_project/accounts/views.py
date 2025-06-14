from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm

CustomUser = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Benvenuto, {user.username}! Il tuo account è stato creato.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Si è verificato un errore durante la registrazione. Controlla i dati inseriti.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form, 'title': 'Registrati'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bentornato, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Nome utente o password non validi.')
        else:
            messages.error(request, 'Nome utente o password non validi.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'title': 'Accedi'})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Hai effettuato il logout con successo.')
    return redirect('login')


def is_store_manager(user):
    return user.is_authenticated and user.is_staff


@login_required
def dashboard(request):

    context = {
        'title': 'Dashboard',
        'is_manager': is_store_manager(request.user),
    }
    return render(request, 'dashboard.html', context)

