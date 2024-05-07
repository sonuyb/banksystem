# authentication/urls.py
 
from django.urls import path
from .views import *
 
urlpatterns = [
    path('verify/', verify.as_view(), name='verify'),
    path('loan-interest/', InterestRateCreateAPIView.as_view(), name='create_interest_rate'),
    path('interest/<int:pk>/', InterestRateUpdateDestroyAPIView.as_view(), name='interest-rate-detail'),
    path('approve/', LoanApprovalAPIView.as_view(), name='loan-approval'),
     path('loan-applied/', UserLoanApplicationListView.as_view(), name='user_loan_applications'),
]