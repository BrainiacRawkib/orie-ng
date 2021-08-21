from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Form to create an Order."""

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'contact', 'address',
            'zip_code', 'city', 'state'
        ]
