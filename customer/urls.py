from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',DashboardApiView.as_view(),name='dashboard'),
    path('savings/', CreateSavingsAccount.as_view(), name='savingsaccountlist'),
    path('current/', CreateCurrentAccountView.as_view(), name='currentAccountList'),
    path('fixedDeposit/', CreateFixedDepositAccountView.as_view(), name='fixedDepositAccountList'),
    path('recurring-deposit/', CreateRecurringDepositAccountView.as_view(), name='recurring-deposit-account-list'),
    path('fixed-deposit-accounts/<int:user_id>', ViewAllFixedDepositAccounts.as_view(), name='fixed_deposit_accounts'), #admin
    path('Recurrent-deposit-accounts/<int:user_id>', ViewAllRecurringDepositAccounts.as_view(), name='Recurrent_deposit_accounts'), #admin
    path('transaction/', TransactionAPIView.as_view(), name='transaction'),
    # path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('banktransfer/', FundTransferView.as_view(), name='fundtransfer'),
    path('loan-applications/', LoanApplicationCreateAPIView.as_view(), name='loan-application-create'), #customer
    path('loans/', InterestListAPIView.as_view(), name='loan_list'), #customer
    path('view-loans/', LoanApplicationListAPIView.as_view(), name='loan-list'), #customer
    path('budgets/', BudgetListCreateAPIView.as_view(), name='budget-list-create'),
     path('transactionhistory/<int:acc>/', TransactionHistoryAPIView.as_view(), name='transaction_history_by_account')
]
