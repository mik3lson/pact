from django.shortcuts import render

from rest_framework import generics
from .models import Invoice
from .serializers import InvoiceSerializer, InvoiceCreateSerializer
from .utils import send_invoice_email
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Invoice
from .serializers import InvoiceSerializer
from .serializers import DashboardSerializer
from accounts.models import User


class InvoiceCreateView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceCreateSerializer

    def perform_create(self, serializer):
        invoice = serializer.save()
        send_invoice_email(invoice)




class InvoiceMockPayView(APIView):
    def post(self, request, reference):
        try:
            invoice = Invoice.objects.get(reference=reference)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

        if invoice.status != 'pending':
            return Response({"error": f"Invoice is already {invoice.status}"}, status=status.HTTP_400_BAD_REQUEST)

        invoice.status = 'funded'
        invoice.funded_at = timezone.now()
        invoice.save()

        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_200_OK)
    


class InvoiceReleaseView(APIView):
    def post(self, request, reference):
        try:
            invoice = Invoice.objects.get(reference=reference)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        requester_email = request.data.get('buyer_email')
        if requester_email != invoice.buyer_email:
            return Response({"error": "Only the buyer can release this payment"}, status=status.HTTP_403_FORBIDDEN)

        if invoice.status != 'funded':
            return Response(
                {"error": f"Cannot release funds — invoice status is '{invoice.status}', expected 'funded'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        invoice.status = 'completed'
        invoice.completed_at = timezone.now()
        invoice.save()

        # TODO: trigger real payout to seller via Alat Pay here later

        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_200_OK)
    


class InvoiceListByBuyerView(generics.ListAPIView):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        buyer_id = self.kwargs['buyer_id']
        return Invoice.objects.filter(buyer_id=buyer_id).order_by('-created_at')
    

class InvoiceListBySellerView(generics.ListAPIView):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Invoice.objects.filter(seller_id=seller_id).order_by('-created_at')
    



class UserDashboardView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(DashboardSerializer(user).data)