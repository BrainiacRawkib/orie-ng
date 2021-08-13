import paystack
import weasyprint
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import View, DetailView, TemplateView
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created, order_status_change_notification

from cart.cart import Cart
from stores.models import Product

gateway = paystack.PaystackGateway(secret_key=settings.PAYSTACK_TEST_SECRET_KEY,
                                   public_key=settings.PAYSTACK_TEST_PUBLIC_KEY)


def get_user_details(request):
    initial_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'contact': request.user.contact,
        'address': request.user.address,
        'zip_code': request.user.zip_code,
        'city': request.user.city,
        'state': request.user.state,
    }
    return initial_data


def get_order_form(data=None, initial_data=None):
    return OrderCreateForm(data=data, initial=initial_data)


def get_cart(request):
    return Cart(request)


def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + '/css/pdf.css'
                                           )])
    return response


class OrderCreateView(View):
    """Form to create an order."""

    def get(self, request, *args, **kwargs):
        order_form = get_order_form(data=None, initial_data=None)
        if request.user.is_authenticated:
            order_form = get_order_form(data=None, initial_data=get_user_details(self.request))
        context = {
            'cart': get_cart(request),
            'order_form': order_form,
            'paystack_public_key': settings.PAYSTACK_TEST_PUBLIC_KEY,
            'title': 'Checkout'
        }
        return render(self.request, 'orders/order_create.html', context)

    def post(self, request, *args, **kwargs):
        cart = get_cart(self.request)

        if self.request.user.is_authenticated:
            order_form = get_order_form(data=self.request.POST, initial_data=get_user_details(self.request))

            if order_form.is_valid():
                order = order_form.save(commit=False)
                if self.request.user.is_authenticated:
                    order.user = self.request.user
                if cart.coupon:
                    order.coupon = cart.coupon
                    order.discount = cart.coupon.discount
                order.save()

                for item in cart:
                    OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['price'], quantity=item['quantity'])
                    product = Product.objects.get(name=item['product'])
                    product.stocks_left -= int(item['quantity'])
                    product.save()
                # clear the cart
                cart.clear()

                # set the order_id in the session
                self.request.session['order_id'] = order.id

                charge = gateway.Transaction.initiate({'email': order.email,
                                                       'amount': str(cart.get_total_price_after_discount() * 100),
                                                       'first_name': order.first_name,
                                                       'last_name': order.last_name,
                                                       'callback_url': request.build_absolute_uri(
                                                           reverse('payments:payment-complete'))})
                order.paystack_id = charge['data']['reference']
                order.save()

                # launch asynchronous task
                order_created.delay(order.id)
                order_status_change_notification.delay(order.id)
                self.request.session['transaction_reference'] = charge['data']['reference']
                link = HttpResponseRedirect(charge['data']['authorization_url'])
                return link


class OrderCreatedView(TemplateView):
    template_name = 'orders/order_created.html'

    def get_order_id(self):
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        return order

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'order': self.get_order_id()
        })


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        context.update({
            'title': f'Order #{order.id}',
            'order': order
        })
        return context
