from django.db import models

from customer.models import LoanApplication

# Create your models here.
class LoanApproval(models.Model):
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE)
    approved_date = models.DateField(auto_now_add=True)
    staff_approval =models.BooleanField(default=False)
    admin_approval =models.BooleanField(default=False)
    new_status = models.CharField(max_length=20, choices=LoanApplication.STATUS_CHOICES)

    def _str_(self):
        return f"{self.loan_application.user.username} - {self.loan_application.loan_type} Approval"
    
class InterestRate(models.Model):
    LOAN_TYPES = [
        ('Personal Loan', 'Personal Loan'),
        ('Home Loan', 'Home Loan'),
        ('Car Loan', 'Car Loan'),
        ('Education Loan', 'Education Loan'),
        # Add more loan types as needed
    ]

    loan_type = models.CharField(max_length=100, choices=LOAN_TYPES, unique=True)
    intrestrate = models.DecimalField(max_digits=5, decimal_places=2)  # Interest rate in percentage

    def _str_(self):
        return f"{self.loan_type} Interest Rate: {self.rate}%"