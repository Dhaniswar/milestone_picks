# views.py
import random
import string
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from user.sendgrid import send_sendgrid_email
from .models import User
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserRegistrationSerializer,
    VerifyOTPSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)


class UserRegistrationView(APIView):
    
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User created successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyOTPView(APIView):
    
    permission_classes = [AllowAny]
    
    
    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            cached_otp = cache.get(email)
            if cached_otp and cached_otp == otp:
                user = User.objects.get(email=email)
                user.is_verified = True
                user.otp = None
                user.save()
                return Response({'message': 'User verified successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    
    permission_classes = [AllowAny]
    
    
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")  # Log validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.filter(email=email).first()
                
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    

class ForgotPasswordView(APIView):
    
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                otp = ''.join(random.choices(string.digits, k=6))
                cache.set(email, otp, timeout=300)  # OTP valid for 5 minutes
                subject = 'Password Reset OTP'
                body = f'Your OTP for password reset is {otp}. It will expire in 5 minutes.'
                
                # Send OTP via SendGrid
                if send_sendgrid_email(subject, body, email):
                    return Response({'message': 'OTP sent to email'}, status=status.HTTP_200_OK)
                return Response({'error': 'Error sending OTP via email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ResetPasswordView(APIView):
    
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            cached_otp = cache.get(email)
            if cached_otp and cached_otp == otp:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)