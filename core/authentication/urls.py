from django.urls import path, include
from authentication.views import RegisterView, LoginView, ForgotPasswordAPIView, ResetPasswordAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('login/refresh', TokenRefreshView.as_view(),name="token_refresh"),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
]
