from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from authentication.permissions import IsCustomer, IsStaffOrAdmin, IsAdmin
from customer.serializers import LoanApplicationSerializer
from loan.serializers import InterestRateSerializer
from .models import *
from .serializers import *
from decimal import Decimal



# Create your views here.
class verify(generics.CreateAPIView):
    permission_classes = [IsStaffOrAdmin]
    def post(self, request):
            return Response("Token is valid.")
        
class InterestRateCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsAdmin]
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer
    # permission_classes = [IsAdminOrStaffUser]
    
class InterestRateUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"Message":"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class LoanApprovalAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsStaffOrAdmin]
    queryset = LoanApproval.objects.all()
    serializer_class = LoanApprovalSerializer

    
class UserLoanApplicationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,IsStaffOrAdmin]
    serializer_class = LoanApplicationSerializer
    # permission_classes = [IsAdminOrStaffUser]

    def get_queryset(self):
        # user = self.request.user
        return LoanApplication.objects.all()