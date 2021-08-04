from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')


class CustomerSignUpForm(UserCreationForm):
    """Registration form to add a new Customer"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=25, help_text='')
    email = forms.EmailField(label='Email', required=True)
    contact = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=150, required=True)
    zip_code = forms.CharField(max_length=20, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus', None)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'contact', 'address',
            'zip_code', 'city', 'state'
        ]

    def save(self, commit=True):
        user = super(CustomerSignUpForm, self).save(commit=False)
        user.is_customer = True
        user.is_active = False
        if commit:
            user.save()
        return user

    def clean_password2(self):
        cd_password1 = self.cleaned_data.get('password1')
        cd_password2 = self.cleaned_data.get('password2')
        if cd_password1 != cd_password2:
            raise forms.ValidationError("Passwords don't match.")
        return cd_password2

    def clean_username(self):
        cd_username = self.cleaned_data.get('username')
        if User.objects.filter(username=cd_username).exists():
            raise forms.ValidationError('Username already exists!')
        return cd_username

    def clean_email(self):
        cd_email = self.cleaned_data.get('email')
        if User.objects.filter(email=cd_email).exists():
            raise forms.ValidationError('Email already exists!')
        return cd_email


class MerchantSignUpForm(UserCreationForm):
    """Registration form to add a new Merchant"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=25, help_text='')
    email = forms.EmailField(label='Email', required=True)
    contact = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=150, required=True)
    zip_code = forms.CharField(max_length=20, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super(MerchantSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus', None)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'contact', 'address',
            'zip_code', 'city', 'state'
        ]

    def save(self, commit=True):
        user = super(MerchantSignUpForm, self).save(commit=False)
        user.is_merchant = True
        user.is_active = False
        if commit:
            user.save()
        return user

    def clean_password2(self):
        cd_password1 = self.cleaned_data.get('password1')
        cd_password2 = self.cleaned_data.get('password2')
        if cd_password1 != cd_password2:
            raise forms.ValidationError("Passwords don't match.")
        return cd_password2

    def clean_username(self):
        cd_username = self.cleaned_data.get('username')
        if User.objects.filter(username=cd_username).exists():
            raise forms.ValidationError('Username already exists!')
        return cd_username

    def clean_email(self):
        cd_email = self.cleaned_data.get('email')
        if User.objects.filter(email=cd_email).exists():
            raise forms.ValidationError('Email already exists!')
        return cd_email


class UserUpdateForm(forms.ModelForm):
    """Form to allow user update user details"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(label='Email', required=True)
    username = forms.CharField(max_length=25, help_text='', widget=forms.TextInput(attrs={'autofocus': 'off'}))
    contact = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=150, required=True)
    zip_code = forms.CharField(max_length=20, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus', None)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'contact', 'address', 'zip_code', 'city', 'state']


class ProfileUpdateForm(forms.ModelForm):
    """Form to allow user update profile details"""
    image = forms.ImageField(label='Photo', widget=forms.ClearableFileInput(attrs={'class': 'border'}))

    class Meta:
        model = Profile
        fields = ['image']
