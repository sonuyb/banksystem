# authentication/serializers.py
 
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_birth = serializers.DateField()
    class Meta:
        model = CustomUser
        fields = ['username', 'email','first_name','last_name', 'password', 'role', 'is_staff','date_of_birth']
 
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
   
    
    
 
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
