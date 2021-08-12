from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse
from stores.models import Product
from coupons.models import Coupon

from .models_choices import ORDER_STATUS


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    paystack_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(blank=False)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='created')

    class Meta:
        ordering = ('-created',)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        # total_cost += self.transport_cost
        return total_cost - total_cost * (self.discount / Decimal(100))

    def get_absolute_url(self):
        return reverse('orders:order-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.pk)

    def get_cost(self):
        return self.price * self.quantity
