# apps/invoices/utils.py
from django.core.mail import send_mail
from django.conf import settings


def send_invoice_email(invoice):
    payment_link = f"{settings.FRONTEND_URL}/pay/{invoice.reference}"

    subject = f"Invoice from {invoice.seller.name}: {invoice.title}"
    message = (
        f"Hi,\n\n"
        f"{invoice.seller.name} has sent you an invoice for '{invoice.title}'.\n"
        f"Total amount: {invoice.total_amount}\n\n"
        f"View and pay securely here:\n{payment_link}\n\n"
        f"This payment is held in escrow until you confirm delivery.\n"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[invoice.buyer_email],
        fail_silently=False,
    )