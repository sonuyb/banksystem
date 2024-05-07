from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken,OutstandingToken
from django.contrib.auth import get_user_model

 
class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
 
    def post(self, request, *args, **kwargs):
        role = request.data.get('role')
        request.data['is_staff'] = role == 'staff'
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
User = get_user_model()
class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
 
    def put(self, request, format=None):
            user = request.user
            data = request.data.copy()
 
            if 'password' in data:
                password = data.pop('password')
                user.set_password(password)
                user.save()
 
            serializer = UserRegistrationSerializer(user, data=data, partial=True)
 
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Profile update successful'}, status=status.HTTP_200_OK)
 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                user.save()  
                refresh_token = RefreshToken.for_user(user)

                return Response({
                    'message': 'Login successful',
                    'access_token': str(refresh_token.access_token),
                    'refresh_token': str(refresh_token),
                })
            else:
                return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            auth_header = request.headers['Authorization']
            refresh_token = request.headers['refresh']
            if refresh_token.startswith('Bearer ') and auth_header.startswith('Bearer '):
                bearer_refresh_token = refresh_token.split('Bearer ')[1]
                RefreshToken(bearer_refresh_token).blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)     
        