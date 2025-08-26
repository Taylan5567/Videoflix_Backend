from .views import RegistrationView, CookieTokenObtainPairView, ActivateAccountView, LogoutView, CookieRefreshView, PasswordresetView, PasswordResetConfirmView
from django.urls import path

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("activate/<str:uidb64>/<str:token>/", ActivateAccountView.as_view(), name="activate"),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordresetView.as_view(), name='password_reset'),
    path('password_confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]