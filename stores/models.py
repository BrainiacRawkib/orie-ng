from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.timezone import now
from tinymce.models import HTMLField

from accounts.models import User
from .exceptions import UserNotAMerchant


def get_product_name(instance, filename):
    name = instance.name
    year = instance.date_added.year
    month = instance.date_added.month
    day = instance.date_added.day
    # return f'products/{name}/{year}/{month}/{day}/{filename}'
    return 'products/{}/{}/{}/{}/{}'.format(name, year, month, day, filename)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('stores:product-listings-by-category', args=[self.slug])

    def __str__(self):
        return f'{self.name}'


class AvailableProductManager(models.Manager):
    def get_queryset(self):
        return super(AvailableProductManager, self).get_queryset().filter(available=True)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to=get_product_name, default='no_image.png')
    image_2 = models.ImageField(upload_to=get_product_name)
    image_3 = models.ImageField(upload_to=get_product_name)
    image_4 = models.ImageField(upload_to=get_product_name)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stocks_left = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    description = HTMLField()
    objects = models.Manager()
    stocked = AvailableProductManager()

    class Meta:
        ordering = ('-date_added',)
        verbose_name_plural = 'Products'

    def get_absolute_url(self):
        return reverse('stores:product-detail', kwargs={'slug': self.slug})

    def created_delta(self):
        return now() - self.date_added

    def get_average_rating_score(self):
        average_score = 0.0
        if self.reviews.count() > 0:
            total_score = sum([review.ratings for review in self.reviews.all()])
            average_score = total_score / self.reviews.count()
        return round(average_score, 1)

    def reviews_count(self):
        return sum(i.get_total() for i in self.reviews.all())

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.merchant.is_customer:
            raise UserNotAMerchant
        return super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f'{self.name}'


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    ratings = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def get_total(self):
        return self.ratings

    def __str__(self):
        return f'{self.product} has {self.ratings} ratings'
