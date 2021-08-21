from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from accounts.decorators import user_created_order
from .views import *


app_name = 'orders'

urlpatterns = [
    # orders urls
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('admin/order/<int:order_id>/pdf/', staff_member_required(invoice_pdf), name='admin-invoice-pdf'),
    path('order/<int:order_id>/pdf/', user_created_order(invoice_pdf), name='user-invoice-pdf'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
