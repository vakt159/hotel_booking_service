from django.urls import path

from payment.views import StripeWebhook, PaymentSuccessView, PaymentCancelView, \
    PaymentListView

app_name = "payments"

urlpatterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("webhook/", StripeWebhook.as_view(), name="stripe-webhook"),
    path("success/", PaymentSuccessView.as_view(), name="success"),
    path("cancel/", PaymentCancelView.as_view(), name="cancel")
]