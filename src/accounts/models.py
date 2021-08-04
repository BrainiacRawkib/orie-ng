from django.contrib.auth.models import AbstractUser
from django.db import models
from .exceptions import MultipleUserAccountException


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_official = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=False)
    is_mvp = models.BooleanField(default=False)
    contact = models.CharField(max_length=15, blank=False, unique=True)
    address = models.CharField(max_length=150, blank=True)
    zip_code = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=20, default='')

    def save(self, *args, **kwargs):
        if self.is_customer and self.is_merchant:
            raise MultipleUserAccountException
        return super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/%Y/%m/%d/', default='avatar.png')

    def __str__(self):
        return f'{self.user.username}'
