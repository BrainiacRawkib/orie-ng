# from django.db import models
# from django.contrib.sessions.models import Session
# from accounts.models import User
# from stores.models import Product
#
#
# class UserCart(models.Model):
#     user = models.OneToOneField(User, related_name='user_cart', on_delete=models.CASCADE)
#     session_key = models.CharField(max_length=40)
#     session_data = models.TextField()
#
#     def __str__(self):
#         return f'{self.user.username} cart'
#
#
# class CartItems(models.Model):
#     user = models.ForeignKey(UserCart, related_name='cart_items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='user_cart_product', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField()
#
#     class Meta:
#         verbose_name_plural = 'Cart Items'
#
#     def __str__(self):
#         return f'{self.user} cart items'
