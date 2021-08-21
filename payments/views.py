import hmac
import hashlib
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View

from orders.models import Order


@require_POST
@csrf_exempt
def paystack_webhook(request):
    """
        The function takes an http request object
        containing the json data from paystack webhook client.
        Django's http request and response object was used
        for this example.
    """
    paystack_sk = settings.PAYSTACK_TEST_SECRET_KEY
    payload = json.loads(request.body)
    computed_hmac = hmac.new(bytes(paystack_sk, 'utf-8'), str.encode(request.body.decode('utf-8')),
                             digestmod=hashlib.sha512).hexdigest()
    # if 'HTTP_X_PAYSTACK_SIGNATURE' in request.META:
    #     if request.META['HTTP_X_PAYSTACK_SIGNATURE'] == computed_hmac \
    #             and request.META['REMOTE_ADDR'] in settings.PAYSTACK_WEBHOOK_IP_ADDRESSES:
            # IMPORTANT! Handle webhook request asynchronously!!
            #
            # ..code
            #
            # pass
    if payload['event'] == 'charge.success':
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        order.paid = True
        order.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)  # non 200


class PaymentCompleteView(TemplateView):
    template_name = 'payments/payment_complete.html'
    extra_context = {'title': 'Transaction Successful'}

    def get(self, request, *args, **kwargs):
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        context = {
            'order': order
        }
        kwargs.update(context)
        return super(PaymentCompleteView, self).get(request, *args, **kwargs)


class PaymentCanceledView(TemplateView):
    template_name = 'payments/payment_canceled.html'
    extra_context = {'title': 'Transaction Error'}
