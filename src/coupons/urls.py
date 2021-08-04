from django.urls import path
from .views import *


app_name = 'coupons'

urlpatterns = [
    path('apply/', CouponApplyView.as_view(), name='coupon-apply'),
]
