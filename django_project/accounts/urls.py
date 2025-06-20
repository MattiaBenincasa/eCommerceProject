from django.urls import path
from .views import (
    UserSignUp,
    SignUpSuccess,
    UserLogin,
    UserLogout,
    LogoutSuccess,
    Dashboard,
    PasswordChange,
    PasswordChangeSuccess
)

urlpatterns = [
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('singup_success/', SignUpSuccess.as_view(), name="signup_success"),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('logout_success/', LogoutSuccess.as_view(), name='logout_success'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change_success/', PasswordChangeSuccess.as_view(), name='password_change_success')
]
