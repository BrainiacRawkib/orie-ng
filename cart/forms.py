from django import forms


class CartAddProductForm(forms.Form):
    """Form to add product to or update product in cart."""

    quantity = forms.IntegerField(min_value=1, max_value=40,
                                  widget=forms.NumberInput(attrs={'class': "form-control text-center px-3", 'value': 1
                                                                  }))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
