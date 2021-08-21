from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    # cart urls
    path('cart-detail/', CartDetailView.as_view(), name='cart-detail'),
    path('cart-add/<int:pk>/', CartAddView.as_view(), name='cart-add'),
    path('cart-remove/<int:pk>/', CartRemoveView.as_view(), name='cart-remove'),
]
