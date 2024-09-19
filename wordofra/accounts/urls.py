from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from accounts.forms import LoginForm

urlpatterns = [
    path('login/', views.user_login, name='login'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('login/', auth_views.LoginView.as_view(
    #     template_name='accounts/login.html',
    #     authentication_form=LoginForm  # Use custom form here
    # ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'), 
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('opt-in/', views.opt_in_newsletter, name='opt_in_newsletter'),
    path('subscription-success/', views.subscription_success, name='subscription_success'),
    # Add more paths like profile or password reset if needed
]
