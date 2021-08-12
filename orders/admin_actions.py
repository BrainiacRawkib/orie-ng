from .tasks import order_status_change_notification


def order_status_change(queryset, status):
    for order in queryset:
        order.order_status = status
        order.save()
        order_status_change_notification.delay(order.id)


def status_processing(modeladmin, request, queryset):
    order_status_change(queryset, 'processing')


status_processing.short_description = 'status_processing'


def status_shipped(modeladmin, request, queryset):
    order_status_change(queryset, 'shipped')


status_shipped.short_description = 'status_shipped'


def status_completed(modeladmin, request, queryset):
    order_status_change(queryset, 'completed')


status_completed.short_description = 'status_completed'
