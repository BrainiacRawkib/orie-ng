from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory, modelform_factory
from .models import Review, Product, ProductImages

REVIEW_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class ReviewForm(forms.ModelForm):
    """Form to allow users review a product."""

    class Meta:
        model = Review
        fields = ['ratings', 'comment']
        widgets = {
            'ratings': forms.RadioSelect,
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control shadow px-2',
                    'rows': 6,
                }
            )
        }


class ProductAddForm(forms.ModelForm):
    available = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'image_2', 'image_3', 'image_4', 'price', 'available', 'description']
        widgets = {
            'image': forms.ClearableFileInput(
                attrs={
                    'multiple': True
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'style': 'resize:none'
                }
            )
        }


class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImages
        fields = ['image']
        # widgets = {
        #     'product': forms.HiddenInput()
        # }


ProductImageForms = modelformset_factory(model=ProductImages, form=ProductImageForm, extra=3)

# ProductImageForms = inlineformset_factory(Product, ProductImages, fields=['im'])