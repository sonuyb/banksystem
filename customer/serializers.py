

from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import LoanApplication

class SavingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = ['id', 'balance', 'created_at']
    

class CurrentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAccount
        fields = ['id', 'balance', 'created_at']

 

class FixedDepositAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedDepositAccount
        fields = ['id', 'amount', 'created_at', 'interest_rate', 'duration_months']

   

class RecurringDepositAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringDepositAccount
        fields = ['id', 'created_at', 'interest_rate', 'installment_amount', 'duration_months']

class TransactionSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = serializers.ChoiceField(choices=('DEPOSIT', 'WITHDRAWAL'))
    description = serializers.CharField(max_length=255, required=False)
    
    # class Meta:
    #     model =Transaction
    #     fields= ['account_number','amount','transaction_type','description']
        
class FundTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundTransfer
        fields = ['sender_account_number', 'receiver_account_number', 'amount', 'timestamp']
        
    def save(self, *args, **kwargs):
        sender_account_number = self.validated_data.get('sender_account_number')
        receiver_account_number = self.validated_data.get('receiver_account_number')
        amount = self.validated_data.get('amount')

        sender_account = Account.objects.get(account_number=sender_account_number)
        receiver_account = Account.objects.get(account_number=receiver_account_number)

        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()
            return super().save(*args, **kwargs)
        else:
            raise serializers.ValidationError("Insufficient balance for fund transfer")


        
class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['loan_type', 'amount', 'duration_months', 'status', 'applied_date']
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Loan amount must be greater than zero.")
        elif value < 5000:
            raise serializers.ValidationError("Loan amount must be at least 5000.")
        return value

    def validate_duration_months(self, value):
        if value <= 0:
            raise serializers.ValidationError("Loan duration must be greater than zero.")
        return value
        
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id','account_number', 'name', 'total_amount', 'start_date', 'end_date']

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'transaction_date', 'description']