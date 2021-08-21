import weasyprint
from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from celery import shared_task
from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    msg = f'Hi {order.first_name, order.last_name}, \n\n' \
        f'You have successfully placed an order. Your order ID is {order.id}'
    email = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [order.email])

    # generate pdf
    html = render_to_string('orders/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach PDF file
    # email.attach(f'order_{order.id}.pdf', out.read(), 'application/pdf')
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    # send email
    return email.send()


@shared_task
def order_status_change_notification(order_id):
    """
    Task to update customers on the Order status.
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    msg = f'Hi {order.first_name, order.last_name}, \n\n' \
        f'Your order {order.id} status has been changed to {order.order_status}'
    send_email = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [order.email])
    # send_email.send()
    return send_email.send()
