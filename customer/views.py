
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
from authentication.permissions import IsCustomer
from loan.models import InterestRate
from loan.serializers import InterestRateSerializer
from .serializers import *
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets
from rest_framework import generics
# from django.http import JsonResponse
from rest_framework import status
import json
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from django.core.mail import send_mail
from .permissions import IsStaffOrAdmin


class CreateSavingsAccount(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsCustomer]
    queryset = SavingsAccount.objects.all()
    serializer_class = SavingsAccountSerializer
    def perform_create(self, serializer):
        # Assign the authenticated user to the account being created
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
 
        # Get the created account instance
        instance = serializer.instance
 
        # Modify the response data to include the account number
        response_data = serializer.data
        response_data['account_number'] = instance.account_number  # Add account number to response
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)



class CreateCurrentAccountView(generics.CreateAPIView):
    queryset = CurrentAccount.objects.all()
    serializer_class = CurrentAccountSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Assign the authenticated user to the account being created
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
 
        # Get the created account instance
        instance = serializer.instance
 
        # Modify the response data to include the account number
        response_data = serializer.data
        response_data['account_number'] = instance.account_number  # Add account number to response
 
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    


class CreateFixedDepositAccountView(generics.CreateAPIView):
     permission_classes = [IsAuthenticated,IsCustomer]
     queryset = FixedDepositAccount.objects.all()
     serializer_class = FixedDepositAccountSerializer
     def perform_create(self, serializer):
        # Assign the authenticated user to the account being created
        serializer.save(user=self.request.user)

     
     def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
     def get(self, request, *args, **kwargs):
        user = request.user
        # Filter fixed deposit accounts based on the logged-in user
        fixed_deposit_accounts = FixedDepositAccount.objects.filter(user=user)
        serializer = FixedDepositAccountSerializer(fixed_deposit_accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateRecurringDepositAccountView(generics.CreateAPIView):    
    permission_classes = [IsAuthenticated,IsCustomer]
    queryset = RecurringDepositAccount.objects.all()
    serializer_class = RecurringDepositAccountSerializer
    def perform_create(self, serializer):
        # Assign the authenticated user to the account being created
        serializer.save(user=self.request.user)

     
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def get(self, request, *args, **kwargs):
        user = request.user
        # Filter fixed deposit accounts based on the logged-in user
        Recurrent_deposit_accounts = RecurringDepositAccount.objects.filter(user=user)
        serializer = RecurringDepositAccountSerializer(Recurrent_deposit_accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
class ViewAllFixedDepositAccounts(generics.ListAPIView):
    queryset = FixedDepositAccount.objects.all()
    serializer_class = FixedDepositAccountSerializer
    permission_classes = [IsStaffOrAdmin]
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')        
        if user_id:
            return FixedDepositAccount.objects.filter(user_id=user_id)        
        else:           
            return FixedDepositAccount.objects.all()
   
class ViewAllRecurringDepositAccounts(generics.ListAPIView):
    queryset = RecurringDepositAccount.objects.all()
    serializer_class = RecurringDepositAccountSerializer
    permission_classes = [IsStaffOrAdmin] 

    def get_queryset(self):
        user_id = self.kwargs.get('user_id') 
        if user_id:
            return RecurringDepositAccount.objects.filter(user_id=user_id)        
        else:           
            return RecurringDepositAccount.objects.all() 
     
class TransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    TRANSACTION_LIMIT = 100000
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data.get('account_number')
            transaction_type = serializer.validated_data.get('transaction_type')
            amount = serializer.validated_data.get('amount')
            description = serializer.validated_data.get('description', '')
 
            try:
                balance_amount= None
                account = Account.objects.get(account_number=account_number)
                if transaction_type == 'DEPOSIT':
                    if amount > self.TRANSACTION_LIMIT:
                        return Response({"message": f"Deposit amount exceeds the transaction limit of {self.TRANSACTION_LIMIT}"}, status=status.HTTP_400_BAD_REQUEST)
                   
                    balance_amount=account.deposit(amount)
                    message = "Deposit successful"
                elif transaction_type == 'WITHDRAWAL':
                    if amount > self.TRANSACTION_LIMIT:
                        return Response({"error": f"Withdrawal amount exceeds the transaction limit of {self.TRANSACTION_LIMIT}"}, status=status.HTTP_400_BAD_REQUEST)
                    if amount > account.balance:
                        return Response({"message": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
                    balance_amount = account.withdraw(amount)
                    message = "Withdrawal successful"
                    budget = Budget.objects.filter(name=description).first()
                    if budget:
                        budget.total_amount -= amount
                        budget.save()
                        if budget.total_amount < 0:
                            subject = 'Budget Exceeded'
                            message = f'Your budget "{budget.name}" has been exceeded.'
                            recipient_list = [request.user.email]  # Assuming each budget has a user field representing the owner
                            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
 
 
                else:
                    return Response({"message": "Invalid transaction type"}, status=status.HTTP_400_BAD_REQUEST)
 
                transaction = Transaction.objects.create(account=account, transaction_type=transaction_type, amount=amount, description=description)
                return Response({"message": message,**( {"balance":balance_amount} if balance_amount else{})}, status=status.HTTP_201_CREATED)
 
            except Account.DoesNotExist:
                return Response({"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class DepositView(APIView):
#     def post(self, request):
#         serializer = DepositWithdrawalSerializer(data=request.data)
#         if serializer.is_valid():
#             account_number = serializer.validated_data['account_number']
#             amount = serializer.validated_data['amount']
#             try:
#                 account = SavingsAccount.objects.get(account_number=account_number)
#             except SavingsAccount.DoesNotExist:
#                 try:
#                     account = CurrentAccount.objects.get(account_number=account_number)
#                 except CurrentAccount.DoesNotExist:
#                     return Response({"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
#             account.deposit(amount)
#             return Response({"message": "Deposit successful"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class WithdrawView(APIView):
#     def post(self, request):
#         serializer = DepositWithdrawalSerializer(data=request.data)
#         if serializer.is_valid():
#             account_number = serializer.validated_data['account_number']
#             amount = serializer.validated_data['amount']
#             try:
#                 account = SavingsAccount.objects.get(account_number=account_number)
#             except SavingsAccount.DoesNotExist:
#                 try:
#                     account = CurrentAccount.objects.get(account_number=account_number)
#                 except CurrentAccount.DoesNotExist:
#                     return Response({"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
#             if amount > account.balance:
#                 return Response({"message": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
                
#             account.withdraw(amount)
#             return Response({"message": "Withdrawal successful"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FundTransferView(APIView):
    permission_classes = [IsAuthenticated,IsCustomer]
    def post(self, request):
        serializer = FundTransferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    # permission_classes = [IsAdminOrStaffUser]

class InterestListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,IsCustomer]
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InterestRate.objects.all()



class LoanApplicationCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsCustomer]
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    # permission_classes = [IsCustomerUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['user'] = request.user

        loan_type = serializer.validated_data['loan_type']

        amount = Decimal(serializer.validated_data['amount'])
        duration_years = Decimal(serializer.validated_data['duration_months']) / Decimal('12')

        try:
            interest_rate_obj = InterestRate.objects.get(loan_type=loan_type)
            interest_rate = Decimal(interest_rate_obj.intrestrate) / Decimal('100')  # Convert to Decimal and percentage
        except InterestRate.DoesNotExist:
            interest_rate = Decimal('0.10')  # Default interest rate of 10%

        monthly_interest_rate = interest_rate / Decimal('12')

        total_payments = duration_years * Decimal('12')

        # Calculate monthly payment (EMI)
        monthly_payment = (amount * monthly_interest_rate) / (Decimal('1') - (Decimal('1') + monthly_interest_rate) ** -total_payments)

        # Calculate total amount payable after loan term
        total_amount_payable = monthly_payment * total_payments

        # Save the loan application
        self.perform_create(serializer)

        # Retrieve the saved loan application instance
        loan_application = serializer.instance

        return Response({
            "loan_details": {
                "Loan Amount": f"Rs {amount}",
                "Tenure": f"{duration_years} years",
                "Interest Rate": f"{interest_rate * 100}%",
                "Total Amount Payable After Loan Term": f"Rs {total_amount_payable}",
                "Monthly Payment (EMI)": f"Rs {monthly_payment}",
                "Applied Date": loan_application.applied_date.strftime("%Y-%m-%d %H:%M:%S"),
                "Status": loan_application.status,
            },
            "message": "Loan application created successfully."
        }, status=status.HTTP_201_CREATED)

class LoanApplicationListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,IsCustomer]
    serializer_class = LoanApplicationSerializer
    # permission_classes = [IsCustomerUser]

    def get_queryset(self):
        # Retrieve the authenticated user
        user = self.request.user
        # Filter loan applications based on the user
        return LoanApplication.objects.filter(user=user)



    # permission_classes = [IsAdminOrStaffUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Update loan application status
        loan_application = serializer.validated_data['loan_application']
        new_status = serializer.validated_data['new_status']
        loan_application.status = new_status
        loan_application.save()

        # Create loan approval instance
        loan_approval = serializer.save()

        send_mail(
            'Loan Approval Notification',
            f'Your loan application for {loan_application.loan_type} has been {new_status.lower()}.',
            'sonuyohannan4@gmail.com',
            [loan_application.user.email],
            fail_silently=True,
        )

        return Response({'message': 'Loan status updated and notification sent'}, status=status.HTTP_201_CREATED)

    
class BudgetListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,IsCustomer]
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    

class BudgetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsCustomer]
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    
class TransactionHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated,IsCustomer]

    def get(self, request,acc):
        try:
            transactions = Transaction.objects.filter(account__account_number=acc)
            serializer = TransactionHistorySerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"message": "No transaction history found for the provided account number"}, status=status.HTTP_404_NOT_FOUND)

class DashboardApiView(generics.ListAPIView):
    serializer_class = SavingsAccountSerializer
    def get_queryset(self):
        user = self.request.user
        accounts = Account.objects.filter(user=user)
        newArray = []
        # for account in accounts:
        #     transactions = Transaction.objects.filter(account__account_number=account.account_number).order_by('-id')[:10]
        #     serializer = TransactionHistorySerializer(transactions, many=True)
        #     newArray.append({'transactions': serializer.data})
        return accounts
    

