from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.generic import TemplateView, View
from .forms import ContactForm


def get_user_details(request):
    user_data = {
        'name': request.user.username,
        'email': request.user.email
    }
    return user_data


class ContactView(View):

    def get_contact_form(self, data=None, initial_data=None):
        return ContactForm(data=data, initial=initial_data)

    def get(self, request, *args, **kwargs):
        contact_form = self.get_contact_form(data=None, initial_data=None)
        if self.request.user.is_authenticated:
            contact_form = self.get_contact_form(data=None, initial_data=get_user_details(self.request))
        context = {
            'form': contact_form,
            'title': 'Contact Us'
        }
        return render(self.request, 'contacts/contact_form.html', context)

    def post(self, request, *args, **kwargs):
        contact_form = self.get_contact_form(data=self.request.POST)
        if contact_form.is_valid():
            subject = 'Notification'
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['message']
            body = message + '\n\nfrom: \n' + name + '\n' + email
            contact_form.save()
            send_email = EmailMessage(subject, body, from_email=email, to=[settings.EMAIL_HOST_USER])
            send_email.send()
            messages.success(self.request, f'Message Sent Successfully!')
        return redirect('contacts:message-sent')


class MessageSentView(TemplateView):
    template_name = 'contacts/message_sent.html'
    extra_context = {'title': 'Sent'}
