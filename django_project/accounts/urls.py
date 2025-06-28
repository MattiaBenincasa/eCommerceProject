from django.urls import path
from .views import (
    UserSignUp,
    SignUpSuccess,
    UserLogin,
    UserLogout,
    LogoutSuccess,
    CustomerDashboard,
    PasswordChange,
    PasswordChangeSuccess,
    StoreManagerDashboard,
    UpdateUserInfo,
    DeleteAccount,
)

urlpatterns = [
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('singup_success/', SignUpSuccess.as_view(), name="signup_success"),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('logout_success/', LogoutSuccess.as_view(), name='logout_success'),
    path('dashboard/', CustomerDashboard.as_view(), name='dashboard'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('update_info/<int:pk>', UpdateUserInfo.as_view(), name='update_user_info'),
    path('password_change_success/', PasswordChangeSuccess.as_view(), name='password_change_success'),
    path('store_manager_dashboard/', StoreManagerDashboard.as_view(), name='store_manager_dashboard'),
    path('account_deactivation/', DeleteAccount.as_view(), name="account_deactivation")
]
