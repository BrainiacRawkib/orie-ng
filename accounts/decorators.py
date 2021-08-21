from orders.models import Order
from django.shortcuts import redirect


def user_created_order(view_func):
    """A decorator to get all orders associated with a user."""

    def wrap(request, *args, **kwargs):
        # get the order_id
        order_id = kwargs["order_id"]
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            if request.user.is_merchant:
                return redirect('accounts:merchants-profile')
            return redirect('accounts:customers-profile')
        return view_func(request, *args, **kwargs)
    return wrap
