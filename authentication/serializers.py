# authentication/serializers.py
 
from rest_framework import serializers
from .models import CustomUser,BlacklistedAccessToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
 
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'is_staff']
 
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
   
    
    
 
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class LogoutSerializer(serializers.Serializer):
     
    token = serializers.CharField()
    user_id = serializers.IntegerField()
         
    def create(self, validated_data):
        blacklisted_token = BlacklistedAccessToken.objects.create(
            token=validated_data['token'],
            user_id=validated_data['user_id']
        )
        return blacklisted_token