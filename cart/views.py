from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .cart import Cart
from .forms import CartAddProductForm
from stores.models import Product
from coupons.forms import CouponApplyForm
from stores.recommender import Recommender


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        form = CartAddProductForm(self.request.POST)
        if form.is_valid() and product.stocks_left > 0:
            cd = form.cleaned_data
            if cd['quantity'] > product.stocks_left:
                cd['quantity'] = product.stocks_left
            cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
            return redirect('cart:cart-detail')
        messages.error(self.request, 'Product not available')
        return redirect('stores:product-detail', product.slug)


class CartDetailView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(self.request)
        r = Recommender()

        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'], 'override': True
            })
        coupon_apply_form = CouponApplyForm()
        cart_products = [item['product'] for item in cart]
        r.products_bought(cart_products)
        recommended_products = []
        if cart_products:
            recommended_products = r.suggest_products_for(cart_products, max_results=6)
        context = {
            'cart': cart,
            'coupon_apply_form': coupon_apply_form,
            'recommended_products': recommended_products,
            'cart_cart': cart.cart,
            'cart_products': cart_products,
            'title': 'Your Cart',
        }
        return render(self.request, 'cart/cart_detail.html', context)


class CartRemoveView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        cart.remove(product)
        return redirect('cart:cart-detail')
