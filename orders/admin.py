from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem
from .admin_actions import status_processing, status_shipped, status_completed


class OrderItemInline(admin.TabularInline):
    """
    Register OrderItem model on the same page with its
    associated Order.
    """
    model = OrderItem


def order_pdf(obj):
    """View Invoice in PDF Format."""

    url = reverse('orders:admin-invoice-pdf', args=[obj.id])
    return mark_safe(f'<a href={url}>PDF</a>')


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Register Order model in the admin site."""

    list_display = [
        'id', 'paystack_id', 'first_name', 'last_name', 'email', 'address', 'zip_code',
        'city', 'created', 'updated', 'order_status', order_pdf
    ]
    list_filter = ['created', 'updated']
    readonly_fields = ['paystack_id']
    inlines = [OrderItemInline]
    actions = [status_processing, status_shipped, status_completed]
    list_per_page = 15
