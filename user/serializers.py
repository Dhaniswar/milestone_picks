from rest_framework import serializers
from .models import User
import logging
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



logger = logging.getLogger(__name__)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
    def validate(self, attrs):
        print(f"Received data: {attrs}")  # Log the input data
        return attrs



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField()




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        #custom claims
        token['is_admin'] = user.is_admin
        token['username'] = user.username
        token['email'] = user.email
        token['is_verified'] = user.is_verified

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['is_admin'] = self.user.is_admin
        data['is_verified'] = self.user.is_verified
        data['username'] = self.user.username
        data['email'] = self.user.email
        
        return data