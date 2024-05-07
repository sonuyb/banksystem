# authentication/urls.py
 
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
 
urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='tokenrefresh'),
    path('update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
]