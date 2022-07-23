from rest_framework import serializers
from .models import Login, User

# Create your serializiers here
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = "__all__"