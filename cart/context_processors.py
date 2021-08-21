from .cart import Cart


def cart(request):
    """Custom context_processor to view the cart items."""
    return {'cart': Cart(request)}
