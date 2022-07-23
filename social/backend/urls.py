from django.urls import path
from . import views

# Create your urls here
urlpatterns = [
    path("create", views.CreateUserAPIView.as_view()),
    path("login", views.login, name="login"),
    path("resend-otp", views.resend_otp, name="resend_otp"),
    
]
