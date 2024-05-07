from django.shortcuts import render
from rest_framework import generics
from authentication.permissions import IsStaffOrAdmin
from customer.models import FixedDepositAccount, RecurringDepositAccount
from customer.serializers import FixedDepositAccountSerializer, RecurringDepositAccountSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# Create your views here.

class ViewAllFixedDepositAccounts(generics.ListAPIView):
    [IsAuthenticated,IsStaffOrAdmin]
    queryset = FixedDepositAccount.objects.all()
    serializer_class = FixedDepositAccountSerializer
    permission_classes = [ IsAdminUser]
    
class ViewAllRecurringDepositAccounts(generics.ListAPIView):
    [IsAuthenticated,IsStaffOrAdmin]
    queryset = RecurringDepositAccount.objects.all()
    serializer_class = RecurringDepositAccountSerializer
    permission_classes = [IsAdminUser]