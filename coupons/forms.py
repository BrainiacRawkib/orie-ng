from django import forms


class CouponApplyForm(forms.Form):
    """Form to apply coupon code."""

    code = forms.CharField(max_length=50)
