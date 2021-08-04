import django_filters
from .models import Product
from django_filters import NumberFilter, CharFilter


class ProductFilter(django_filters.FilterSet):
    # price = NumberFilter()

    class Meta:
        model = Product
        fields = [
            'price', 'available'
        ]
