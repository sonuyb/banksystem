# authentication/urls.py
 
from django.urls import path
from .views import *
 
urlpatterns = [
    path('fixed-deposit-accounts/', ViewAllFixedDepositAccounts.as_view(), name='fixed_deposit_accounts'),
    path('Recurrent-deposit-accounts/', ViewAllRecurringDepositAccounts.as_view(), name='Recurrent_deposit_accounts') 
]