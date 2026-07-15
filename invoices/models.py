# apps/invoices/models.py
from django.db import models
from accounts.models import User
import uuid

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('funded', 'Funded'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    invoice_id = models.AutoField(primary_key=True)
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices_created')
    buyer_email = models.EmailField(max_length=100, null=False)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices_received')

    title = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    funded_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.buyer_email} ({self.status})"

    @property
    def total_amount(self):
        return sum(item.total_amount for item in self.items.all())


class InvoiceItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')

    description = models.CharField(max_length=255, null=False)  # e.g. "Logo design" or "T-shirt (Large)"
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False)  # unit price
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} x{self.quantity}"