from django.contrib.auth import views
from django.urls import path
from .views import *


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('home/', home, name='home'),
    path('redirect_to_tasks/', redirect_to_tasks, name='redirect_to_tasks'),
    path('redirect_to_login/', redirect_to_login, name='redirect_to_login'),
    path('edit_profile/', profile_edit, name='profile_edit'),
]
