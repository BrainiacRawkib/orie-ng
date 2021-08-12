from django.urls import path
from .views import *


app_name = 'payments'

urlpatterns = [
    path('webhook/', paystack_webhook, name='paystack-webhook'),
    path('process/', PaymentProcessView.as_view(), name='payment-process'),
    path('complete/', PaymentCompleteView.as_view(), name='payment-complete'),
    path('canceled/', PaymentCanceledView.as_view(), name='payment-canceled'),
]
