from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout

from .serializers import UserSerializer, LoginSerializer, ResendOTPSerializer
from .models import User
from .utils import send_otp, generate_username, verify_otp, resend_otp

# Create your views here.

class CreateUserAPIView(generics.CreateAPIView):
    # This View Creates a New User is User does not exsist in the DATABASE

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

        # Send OTP
        sms = send_otp(str(phone_number))
        print(phone_number)

        try:
            # Check if user has already been created
            registered_user = User.objects.get(phone_number=phone_number)
            if registered_user:

                token, created = Token.objects.get_or_create(user=registered_user)
                return Response({
                    "data": {
                    "user_id": registered_user.id,
                    "phone_number": registered_user.phone_number,
                    "username": registered_user.username,
                    "token": token.key   
                    },
                    "message": "Sms {} to exsisting user".format(sms["message"])      
                })

        except:
            # Create a New User
            user = User.objects.create(
                full_name = full_name,
                phone_number = phone_number,
                username = username,
                dob=dob
            )
            user.save()

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "data": {
                "user": user.id,
                "phone_number": user.phone_number,
                "username": user.username,
                "token": token.key
                },
                "message": "New User created succefully and sms {}".format(sms["message"])
            })


       
@api_view(["POST"])
def resend_otp(request):
    # This View helps in resending OTP after 60 seconds

    serializer = ResendOTPSerializer(data = request.data)

    if serializer.is_valid(raise_exception=True):
        phone_number = serializer.validated_data["phone_number"]

        # Cancel and resend OTP
        sms = resend_otp(str(phone_number))
        return Response({"message": sms["message"]})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
def login_view(request):

    # This View helps OTP Verification and logging in a user
    # An authorization token is sent back as a response and is to be included in headers

    serializer = LoginSerializer(data = request.data)

    if serializer.is_valid(raise_exception=True):
        phone_number = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["code"]

        # Get user attempting to login
        user = User.objects.get(phone_number = phone_number)

        # Verify OTP
        sms = verify_otp(str(phone_number), otp)

        # If OTP is approved authenticate user and return authorization token
    
        if sms["message"] == "approved":

            # Login user
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "data": {
                "phone_number": user.phone_number,
                "token": token.key,
                "user_id": user.pk,
                },
                "message": "User logged in successfully!"
            })
        
        else:
            return Response({"message": "Invalid OTP"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_view(request):

    # This View logs out authenticated user
    # Could be POST method also

    request.user.auth_token.delete()

    logout(request)

    return Response({"message": "User Logged out successfully"})

    

