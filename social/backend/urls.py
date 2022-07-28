from django.urls import path
from . import views

# Create your urls here
urlpatterns = [
    path("user-create", views.CreateUserAPIView.as_view()),
    path("user-login", views.login_view, name="login"),
    path("user-logout", views.logout_view, name="logout"),
    path("user-resend-otp", views.resend_otp, name="resend_otp"),
    
]
