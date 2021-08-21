from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from ..models import User
from ..forms import LoginForm


class SignUpView(TemplateView):
    """Sign up a new user."""

    template_name = 'accounts/registration/signup.html'
    extra_context = {'title': 'Account Type'}


class UserLoginView(SuccessMessageMixin, auth_views.LoginView):
    """Logs a user in."""

    form_class = LoginForm
    extra_context = {'title': 'Login'}
    success_message = 'Access Granted'
    template_name = 'accounts/auths/user_login.html'

    def get_success_url(self):
        return reverse_lazy('stores:product-listings')


class AccountDeactivateView(LoginRequiredMixin, TemplateView, View):
    """Deactivates a user account."""

    template_name = 'accounts/auths/account_deactivate.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'title': 'Deactivate Account'
        })

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        user.is_active = False
        user.save()
        messages.success(request, f'Account Deactivated!')
        return redirect('stores:product-listings')


def logout_request(request):
    """Logout a user."""

    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('stores:product-listings')


class PasswordChangeView(auth_views.PasswordChangeView):
    """Changes password for a user."""

    template_name = 'accounts/auths/password_change.html'
    extra_context = {'title': 'Change Password'}
    success_url = reverse_lazy('accounts:password-change-done')


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    """Password change complete."""

    template_name = 'accounts/auths/password_change_done.html'
    extra_context = {'title': 'Password Change Done'}


class PasswordResetView(auth_views.PasswordResetView):
    """Reset password form for Forgotten passwords."""

    template_name = 'accounts/auths/password_reset_form.html'
    extra_context = {'title': 'Password Reset'}
    success_url = reverse_lazy('accounts:password-reset-done')
    email_template_name = 'accounts/auths/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """A link sent to user's email to reset the password."""

    template_name = 'accounts/auths/password_reset_done.html'
    extra_context = {'title': 'Password Reset Done'}


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Confirm the link sent for resetting password."""

    template_name = 'accounts/auths/password_reset_confirm.html'
    extra_context = {'title': 'Password Reset Confirm'}
    success_url = reverse_lazy('accounts:password-reset-complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """Successfully reset password."""

    template_name = 'accounts/auths/password_reset_complete.html'
    extra_context = {'title': 'Password Reset Complete'}
