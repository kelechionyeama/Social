from rest_framework import serializers
from .models import Login, User, ResendOTP

# Create your serializiers here
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = "__all__"

class ResendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResendOTP
        fields = "__all__"