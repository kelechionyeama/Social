from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer, LoginSerializer
from .models import User
from .utils import send_otp, generate_username, verify_otp, resend_otp

# Create your views here.

class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get user data
        full_name = serializer.validated_data["full_name"]
        phone_number = serializer.validated_data["phone_number"]
        dob = serializer.validated_data["dob"]
        username = full_name[:3] + generate_username()

        # Create a New User
        user = User.objects.create(
            full_name = full_name,
            phone_number = phone_number,
            username = username,
            dob=dob
        )

        user.save()

        # Send OTP
        sms = send_otp(str(phone_number))
        print(phone_number)

        return Response({"message": "User created successfully and OTP {}".format(sms["message"])})

 
@api_view(["POST"])
def resend_otp(request):
    serializer = LoginSerializer(data = request.data)

    if serializer.is_valid(raise_exception=True):
        phone_number = serializer.validated_data["phone_number"]

        # Cancel and resend OTP
        sms = resend_otp(str(phone_number))
        return Response({"message": sms["message"]})



@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data = request.data)

    if serializer.is_valid(raise_exception=True):
        phone_number = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["code"]

        # Get user attempting to login
        user = User.objects.get(phone_number = phone_number)

        # Verify OTP
        sms = verify_otp(str(phone_number), otp)

        # If OTP is approved authenticate user
        if sms["message"] == "approved":
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "phone_number": user.phone_number,
                "token": token.key,
                "user_id": user.pk
            })
        
        else:
            return Response({"message": "Invalid OTP"})


