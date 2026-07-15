# apps/invoices/urls.py

from django.urls import path
from .views import InvoiceCreateView, InvoiceListByBuyerView, InvoiceListBySellerView, InvoiceMockPayView, InvoiceReleaseView, UserDashboardView

urlpatterns = [
    path('invoices/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoices/<uuid:reference>/pay/', InvoiceMockPayView.as_view(), name='invoice-mock-pay'),
    path('invoices/<uuid:reference>/release/', InvoiceReleaseView.as_view(), name='invoice-release'),
    path('users/<int:buyer_id>/invoices-as-buyer/', InvoiceListByBuyerView.as_view(), name='buyer-invoices'),
    path('users/<int:seller_id>/invoices-as-seller/', InvoiceListBySellerView.as_view(), name='seller-invoices'),
    path('users/<int:user_id>/dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
]