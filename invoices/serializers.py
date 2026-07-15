# apps/invoices/serializers.py
from rest_framework import serializers
from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['item_id', 'description', 'quantity', 'amount', 'total_amount']
        read_only_fields = ['item_id', 'total_amount']


class InvoiceCreateSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['seller', 'reference', 'buyer_email', 'title', 'description', 'items','invoice_id', 'status', 'created_at']
        read_only_fields = ['reference', 'invoice_id', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice


class InvoiceSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.name', read_only=True)
    seller_email = serializers.CharField(source='seller.email', read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'invoice_id', 'reference', 'seller', 'seller_name', 'seller_email',
            'buyer_email', 'buyer', 'title', 'description', 'items', 'total_amount',
            'status', 'created_at', 'funded_at', 'completed_at',
        ]
        read_only_fields = ['invoice_id', 'reference', 'status', 'created_at', 'funded_at', 'completed_at']


# apps/invoices/serializers.py
class DashboardSerializer(serializers.Serializer):
    as_seller = serializers.SerializerMethodField()
    as_buyer = serializers.SerializerMethodField()

    def get_as_seller(self, user):
        invoices = Invoice.objects.filter(seller=user).order_by('-created_at')
        return self._summarize(invoices)

    def get_as_buyer(self, user):
        invoices = Invoice.objects.filter(buyer=user).order_by('-created_at')
        return self._summarize(invoices)

    def _summarize(self, invoices):
        return {
            'total_invoices': invoices.count(),
            'pending': invoices.filter(status='pending').count(),
            'funded': invoices.filter(status='funded').count(),
            'completed': invoices.filter(status='completed').count(),
            'total_value': sum(inv.total_amount for inv in invoices),
            'invoices': InvoiceSerializer(invoices, many=True).data,
        }