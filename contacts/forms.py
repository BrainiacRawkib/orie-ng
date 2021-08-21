from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """Form to allow suggestions and complaints."""

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
