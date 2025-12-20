from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView  # 🔒 CHANGED
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Registration endpoint
    path('register/', RegisterView.as_view(), name='register'),

    # 🔒 CHANGED: Login now blocks unverified users
    path('login/', LoginView.as_view(), name='login'),

    # Refresh JWT token
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    # Email verification endpoint
    path('verify/<int:uid>/<str:token>/', VerifyEmailView.as_view()),
]
