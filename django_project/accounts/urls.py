from django.urls import path
from .views import UserSignUp, SignUpSuccess, UserLogin, UserLogout, LogoutSuccess, Dashboard

urlpatterns = [
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('singup_success/', SignUpSuccess.as_view(), name="signup_success"),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('logout_success/', LogoutSuccess.as_view(), name='logout_success'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
]
