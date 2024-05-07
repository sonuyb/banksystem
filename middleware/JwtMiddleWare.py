from rest_framework import exceptions,status
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
class JwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        response = self.verify_token(request)
        if response:
            return response
        return self.get_response(request)
    def verify_token(self, request):
        print('Authorization' in request.headers)
        if 'Authorization' in request.headers:
            print("inside if")
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                bearer_token = auth_header.split('Bearer ')[1]
                if len(bearer_token):
                    try:
                        user, token = self.jwt_authentication.authenticate(request)
                        request.user = user
                        return None  # Token verification successful, continue with the request
                    except exceptions.AuthenticationFailed as e:
                        print("Error: " , e)
                        return JsonResponse({'detail': 'Authentication credentials were not provided.','error':str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return None