from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth.models import Group


class UserSignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("signup_success")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        customer_group = Group.objects.get(name='customer')
        user.groups.add(customer_group)

        return super().form_valid(form)


class UserLogin(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user
        print(user.groups.filter(name='store_manager').exists())
        if user.groups.filter(name='store_manager').exists():
            return reverse_lazy('store_manager_dashboard')
        else:
            return reverse_lazy('HomePage')


class UserLogout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('logout_success')


class LogoutSuccess(TemplateView):
    template_name = 'registration/logout_success.html'


class SignUpSuccess(TemplateView):
    template_name = 'registration/signup_success.html'


class CustomerDashboard(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'registration/dashboard.html'
    permission_required = 'accounts.can_access_customer_dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['is_manager'] = self.request.user.is_staff
        return context


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_success')
    template_name = 'registration/password_change.html'


class PasswordChangeSuccess(LoginRequiredMixin, TemplateView):
    template_name = 'registration/password_change_success.html'


class StoreManagerDashboard(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'store_manager/store_manager_dashboard.html'
    permission_required = 'accounts.can_access_manager_dashboard'

