from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import  LoanApproval,InterestRate

class InterestRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestRate
        fields = ['loan_type','intrestrate']

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApproval
        fields = ['loan_application', 'new_status', ]