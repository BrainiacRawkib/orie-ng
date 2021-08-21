from django.urls import path
from .views import *


app_name = 'payments'

urlpatterns = [
    # payment urls
    path('webhook/', paystack_webhook, name='paystack-webhook'),
    path('complete/', PaymentCompleteView.as_view(), name='payment-complete'),
    path('canceled/', PaymentCanceledView.as_view(), name='payment-canceled'),
]
