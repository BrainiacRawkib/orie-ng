from .tasks import order_status_change_notification


def order_status_change(queryset, status):
    """Admin actions to change Order status."""
    for order in queryset:
        order.order_status = status
        order.save()
        order_status_change_notification.delay(order.id)


def status_processing(modeladmin, request, queryset):
    """Change Order status from created to processing."""
    order_status_change(queryset, 'processing')


status_processing.short_description = 'status_processing'


def status_shipped(modeladmin, request, queryset):
    """Change Order status to shipped."""
    order_status_change(queryset, 'shipped')


status_shipped.short_description = 'status_shipped'


def status_completed(modeladmin, request, queryset):
    """Change Order status to completed."""
    order_status_change(queryset, 'completed')


status_completed.short_description = 'status_completed'
