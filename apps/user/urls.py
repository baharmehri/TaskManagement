from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.user import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('login/type', views.CheckLoginTypeView.as_view(), name='login-type'),
]
