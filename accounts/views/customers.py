from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, TemplateView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ..models import User
from ..forms import CustomerSignUpForm, UserUpdateForm, ProfileUpdateForm


UserModel = get_user_model()


class CustomerSignUpView(CreateView):
    """New user to sign up as a customer."""

    model = User
    form_class = CustomerSignUpForm
    template_name = 'accounts/customers/customer_signup.html'
    extra_context = {'title': 'Customer Signup'}

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Customer'
        return super(CustomerSignUpView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Orieng Confirm Your Email'
        activation_context = {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'protocol': self.request.scheme,
        }
        message = get_template('accounts/auths/activate_account.html').render(activation_context)
        to_email = user.email
        send_mail = EmailMessage(mail_subject, message, to=[to_email])
        send_mail.content_subtype = 'html'
        send_mail.send()
        messages.info(self.request, 'Please Confirm your email address')
        return redirect('accounts:account-signin')


class AccountActivateView(View):
    """Activate account through email."""

    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(self.kwargs.get('uidb64')).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, self.kwargs.get('token')):
            user.is_active = True
            user.save()
            messages.success(self.request, 'Email Successfully Confirmed')
            return redirect('accounts:account-signin')
        else:
            messages.error(self.request, 'Invalid Activation Link')
            return redirect('accounts:account-signup')


class CustomerProfileView(LoginRequiredMixin, TemplateView, View):
    """A Customer should view its Profile."""

    template_name = 'accounts/customers/customer_profile.html'

    def get_user_formset(self, data=None):
        return UserUpdateForm(instance=self.request.user, data=data)

    def get_profile_formset(self, data=None, files=None):
        return ProfileUpdateForm(instance=self.request.user.profile, data=data, files=files)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'user_form': self.get_user_formset(),
            'profile_form': self.get_profile_formset(),
            'title': 'Profile',
        })

    def post(self, request, *args, **kwargs):
        user_formset = self.get_user_formset(data=request.POST)
        profile_formset = self.get_profile_formset(data=request.POST, files=request.FILES)

        if user_formset.is_valid() and profile_formset.is_valid():
            user_formset.save()
            profile_formset.save()
            messages.success(request, 'Account Updated!')
            return redirect('accounts:customers-profile')
        return self.render_to_response({
            'user_form': user_formset,
            'profile_form': profile_formset,
            'title': 'Profile',
        })


class ListCustomersProfileView(ListView):
    """List all customers."""

    model = User
    template_name = 'accounts/customers/list_customers_profile.html'
    context_object_name = 'customers'
    extra_context = {'title': 'All Customers'}
    paginate_by = 20

    def get_queryset(self):
        return User.objects.filter(is_customer=True)


class ViewCustomerProfileView(DetailView):
    """View individual customer's profile."""

    model = User
    template_name = 'accounts/customers/view_customer_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(ViewCustomerProfileView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context.update({
            'title': f'{user.username} Profile',
            'customer': user
        })
        return context
